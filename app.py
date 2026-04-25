import io
import base64
import os
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, QueryLog, LocationStats, User
from weather_analysis import (
    load_weather_data,
    filter_by_rainfall_threshold,
    filter_high_temperature_days,
    filter_by_location,
    analyze_rain_patterns,
    find_max_temperature,
    find_min_temperature,
)
from weather_analysis.visualization import (
    plot_temperature_distribution,
    plot_rainfall_patterns,
    plot_temperature_vs_humidity,
    plot_wind_speed_distribution,
    plot_pressure_vs_rain,
    plot_temperature_range_trends,
)
from weather_analysis.prediction import get_or_train_model, predict_rain, FEATURE_COLUMNS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, 'static', 'img')
DATA_PATH = os.path.join(BASE_DIR, 'AustraliaWeatherData', 'Weather Training Data.csv')
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
SESSION_CSV_KEY = 'uploaded_csv_path'
MAX_UPLOAD_BYTES = 50 * 1024 * 1024
REQUIRED_COLUMNS = {'Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'RainToday'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "weather_app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'weather-analysis-cs3270'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Data loading. Once at startup then held in module level variable
_weather_data = None
_locations = None


def get_data():
    """Return cached dataset and sorted location list, load if needed"""
    global _weather_data, _locations
    if _weather_data is None:
        _weather_data = load_weather_data(DATA_PATH)
        _locations = sorted({row['Location'] for row in _weather_data if row.get('Location')})
    return _weather_data, _locations


# Helpers

def _numeric_avg(values):
    """Return mean of list of floats, or none if empty"""
    valid = [v for v in values if v is not None and isinstance(v, (int, float))]
    return round(sum(valid) / len(valid), 2) if valid else None


def _compute_overall_stats(data):
    """Compute summary statistics for full or filtered dataset"""
    total = len(data)
    avg_max = _numeric_avg([r.get('MaxTemp') for r in data])
    avg_min = _numeric_avg([r.get('MinTemp') for r in data])
    avg_rain = _numeric_avg([r.get('Rainfall') for r in data])
    rainy = sum(1 for r in data if r.get('RainToday') == 'Yes')
    rainy_pct = round(rainy / total * 100, 1) if total else 0
    max_t = find_max_temperature(data)
    min_t = find_min_temperature(data)
    return {
        'total': total,
        'avg_max_temp': avg_max,
        'avg_min_temp': avg_min,
        'avg_rainfall': avg_rain,
        'rainy_days': rainy,
        'rainy_day_pct': rainy_pct,
        'max_temp_ever': round(max_t, 1) if max_t != float('-inf') else None,
        'min_temp_ever': round(min_t, 1) if min_t != float('inf') else None,
    }


def _get_or_cache_location_stats(location, data):
    """Return LocationStats from DB cache, compute and save if missing"""
    cached = LocationStats.query.filter_by(location=location).first()
    if cached:
        return cached

    loc_data = filter_by_location(data, location)
    total = len(loc_data)
    if total == 0:
        return None

    avg_max = _numeric_avg([r.get('MaxTemp') for r in loc_data])
    avg_min = _numeric_avg([r.get('MinTemp') for r in loc_data])
    avg_rain = _numeric_avg([r.get('Rainfall') for r in loc_data])
    max_t = find_max_temperature(loc_data)
    min_t = find_min_temperature(loc_data)
    rainy = sum(1 for r in loc_data if r.get('RainToday') == 'Yes')
    rainy_pct = round(rainy / total * 100, 1)
    avg_wind = _numeric_avg([r.get('WindGustSpeed') for r in loc_data])

    stats = LocationStats(
        location=location,
        total_records=total,
        avg_max_temp=avg_max,
        avg_min_temp=avg_min,
        avg_rainfall=avg_rain,
        max_temp_ever=round(max_t, 1) if max_t != float('-inf') else None,
        min_temp_ever=round(min_t, 1) if min_t != float('inf') else None,
        rainy_days=rainy,
        rainy_day_pct=rainy_pct,
        avg_wind_speed=avg_wind,
    )
    db.session.add(stats)
    db.session.commit()
    return stats


PLOT_DEFINITIONS = [
    ('temperature_distribution.png', 'Temperature Distribution',
     'Distribution of maximum temperatures across all records.'),
    ('rainfall_patterns.png', 'Rainfall Patterns',
     'Distribution of rainfall amounts on rainy days.'),
    ('temp_vs_humidity.png', 'Temperature vs Humidity',
     'Scatter plot showing the relationship between temperature and afternoon humidity.'),
    ('wind_speed_distribution.png', 'Wind Speed Distribution',
     'Distribution of peak wind gust speeds.'),
    ('pressure_vs_rain.png', 'Pressure vs Rain',
     'Atmospheric pressure comparison between rainy and dry days.'),
    ('temperature_range_trends.png', 'Temperature Range Trends',
     'Distribution of daily temperature ranges (Max - Min).'),
]


def _plots_exist():
    return all(os.path.exists(os.path.join(IMG_DIR, fname)) for fname, _, _ in PLOT_DEFINITIONS)


def _generate_plots(data):
    """Generate visualizations into static/img/"""
    os.makedirs(IMG_DIR, exist_ok=True)
    plot_temperature_distribution(data, os.path.join(IMG_DIR, 'temperature_distribution.png'))
    plot_rainfall_patterns(data, os.path.join(IMG_DIR, 'rainfall_patterns.png'))
    plot_temperature_vs_humidity(data, os.path.join(IMG_DIR, 'temp_vs_humidity.png'))
    plot_wind_speed_distribution(data, os.path.join(IMG_DIR, 'wind_speed_distribution.png'))
    plot_pressure_vs_rain(data, os.path.join(IMG_DIR, 'pressure_vs_rain.png'))
    plot_temperature_range_trends(data, os.path.join(IMG_DIR, 'temperature_range_trends.png'))


def get_model():
    """Return trained prediction model, training on first call"""
    data, _ = get_data()
    return get_or_train_model(data)


def _fig_to_b64(fig) -> str:
    """matplotlib Figure to a base64 PNG string"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return encoded


def _build_charts_and_summary(category: str, city: str, city_data: list) -> tuple:
    """Build category specific charts as base64 PNG and a text summary"""
    charts = []

    if category == 'temperature':
        max_temps = [r['MaxTemp'] for r in city_data if r.get('MaxTemp') is not None]
        min_temps = [r['MinTemp'] for r in city_data if r.get('MinTemp') is not None]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(max_temps, bins=30, color='#ef4444', edgecolor='#1e293b', alpha=0.85)
        ax.set_title(f'Max Temperature Distribution — {city}', color='white')
        ax.set_xlabel('Max Temperature (°C)', color='#94a3b8')
        ax.set_ylabel('Frequency', color='#94a3b8')
        ax.tick_params(colors='#94a3b8')
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#161b22')
        for spine in ax.spines.values():
            spine.set_edgecolor('#30363d')
        charts.append(_fig_to_b64(fig))

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(min_temps, bins=30, color='#38bdf8', edgecolor='#1e293b', alpha=0.85)
        ax.set_title(f'Min Temperature Distribution — {city}', color='white')
        ax.set_xlabel('Min Temperature (°C)', color='#94a3b8')
        ax.set_ylabel('Frequency', color='#94a3b8')
        ax.tick_params(colors='#94a3b8')
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#161b22')
        for spine in ax.spines.values():
            spine.set_edgecolor('#30363d')
        charts.append(_fig_to_b64(fig))

        avg_max = _numeric_avg(max_temps)
        avg_min = _numeric_avg(min_temps)
        rec_high = round(max(max_temps), 1) if max_temps else 'N/A'
        rec_low = round(min(min_temps), 1) if min_temps else 'N/A'
        summary = (
            f"{city} — {len(city_data):,} records. "
            f"Avg max temp: {avg_max}°C | Avg min temp: {avg_min}°C. "
            f"Record high: {rec_high}°C | Record low: {rec_low}°C."
        )

    elif category == 'rainfall':
        rainy_rows = [r for r in city_data if r.get('RainToday') == 'Yes']
        dry_rows = [r for r in city_data if r.get('RainToday') == 'No']
        rainfall_amounts = [r['Rainfall'] for r in rainy_rows if r.get('Rainfall') is not None]

        fig, ax = plt.subplots(figsize=(8, 4))
        if rainfall_amounts:
            ax.hist(rainfall_amounts, bins=30, color='#34d399', edgecolor='#1e293b', alpha=0.85)
        ax.set_title(f'Rainfall Distribution on Rainy Days — {city}', color='white')
        ax.set_xlabel('Rainfall (mm)', color='#94a3b8')
        ax.set_ylabel('Frequency', color='#94a3b8')
        ax.tick_params(colors='#94a3b8')
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#161b22')
        for spine in ax.spines.values():
            spine.set_edgecolor('#30363d')
        charts.append(_fig_to_b64(fig))

        fig, ax = plt.subplots(figsize=(6, 4))
        labels = ['Rainy Days', 'Dry Days']
        counts = [len(rainy_rows), len(dry_rows)]
        colors = ['#34d399', '#94a3b8']
        bars = ax.bar(labels, counts, color=colors, edgecolor='#1e293b')
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                    str(count), ha='center', color='white', fontsize=10)
        ax.set_title(f'Rainy vs Dry Days — {city}', color='white')
        ax.set_ylabel('Days', color='#94a3b8')
        ax.tick_params(colors='#94a3b8')
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#161b22')
        for spine in ax.spines.values():
            spine.set_edgecolor('#30363d')
        charts.append(_fig_to_b64(fig))

        total = len(city_data)
        rainy_pct = round(len(rainy_rows) / total * 100, 1) if total else 0
        total_rain = round(sum(rainfall_amounts), 1) if rainfall_amounts else 0
        avg_rain = round(sum(rainfall_amounts) / len(rainfall_amounts), 2) if rainfall_amounts else 0
        summary = (
            f"{city} — {total:,} records. "
            f"Rainy days: {len(rainy_rows):,} ({rainy_pct}%). "
            f"Total rainfall: {total_rain} mm | Avg on rainy days: {avg_rain} mm."
        )

    else:  # extreme
        wind_speeds = [r['WindGustSpeed'] for r in city_data if r.get('WindGustSpeed') is not None]
        max_temps = [r['MaxTemp'] for r in city_data if r.get('MaxTemp') is not None]
        paired = [(r['MaxTemp'], r['WindGustSpeed']) for r in city_data
                  if r.get('MaxTemp') is not None and r.get('WindGustSpeed') is not None]

        fig, ax = plt.subplots(figsize=(8, 4))
        if wind_speeds:
            ax.hist(wind_speeds, bins=30, color='#f59e0b', edgecolor='#1e293b', alpha=0.85)
        ax.set_title(f'Wind Gust Speed Distribution — {city}', color='white')
        ax.set_xlabel('Wind Gust Speed (km/h)', color='#94a3b8')
        ax.set_ylabel('Frequency', color='#94a3b8')
        ax.tick_params(colors='#94a3b8')
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#161b22')
        for spine in ax.spines.values():
            spine.set_edgecolor('#30363d')
        charts.append(_fig_to_b64(fig))

        fig, ax = plt.subplots(figsize=(8, 4))
        if paired:
            xs, ys = zip(*paired)
            ax.scatter(xs, ys, color='#f59e0b', alpha=0.4, s=15, edgecolors='none')
        ax.set_title(f'Max Temp vs Wind Gust Speed — {city}', color='white')
        ax.set_xlabel('Max Temperature (°C)', color='#94a3b8')
        ax.set_ylabel('Wind Gust Speed (km/h)', color='#94a3b8')
        ax.tick_params(colors='#94a3b8')
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#161b22')
        for spine in ax.spines.values():
            spine.set_edgecolor('#30363d')
        charts.append(_fig_to_b64(fig))

        heat_days = sum(1 for t in max_temps if t > 35)
        high_wind_days = sum(1 for w in wind_speeds if w > 60)
        avg_wind = _numeric_avg(wind_speeds)
        summary = (
            f"{city} — {len(city_data):,} records. "
            f"Extreme heat days (>35°C): {heat_days:,}. "
            f"High-wind days (>60 km/h gusts): {high_wind_days:,}. "
            f"Avg wind gust: {avg_wind} km/h."
        )

    return charts, summary


# Auth Routes

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('upload'))
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('upload'))
        error = 'Invalid username or password.'
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    csv_path = session.pop(SESSION_CSV_KEY, None)
    if csv_path and os.path.exists(csv_path):
        os.remove(csv_path)
    logout_user()
    return redirect(url_for('login'))


# Upload Route

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    error = None
    if request.method == 'POST':
        f = request.files.get('csv_file')
        if not f or f.filename == '':
            error = 'No file selected.'
        elif not f.filename.lower().endswith('.csv'):
            error = 'Only .csv files are accepted.'
        else:
            content = f.read(MAX_UPLOAD_BYTES + 1)
            if len(content) > MAX_UPLOAD_BYTES:
                error = 'File exceeds 50 MB limit.'
            else:
                os.makedirs(UPLOAD_DIR, exist_ok=True)
                filename = f'upload_{current_user.id}_{int(datetime.utcnow().timestamp())}.csv'
                save_path = os.path.join(UPLOAD_DIR, filename)
                with open(save_path, 'wb') as out:
                    out.write(content)
                try:
                    sample = load_weather_data(save_path)
                    if not sample:
                        raise ValueError('CSV contains no data rows.')
                    cols = set(sample[0].keys())
                    missing = REQUIRED_COLUMNS - cols
                    if missing:
                        raise ValueError(f'Missing required columns: {", ".join(sorted(missing))}')
                    old = session.get(SESSION_CSV_KEY)
                    if old and os.path.exists(old) and old != save_path:
                        os.remove(old)
                    session[SESSION_CSV_KEY] = save_path
                    return redirect(url_for('interactive_dashboard'))
                except Exception as e:
                    os.remove(save_path)
                    error = str(e)
    return render_template('upload.html', error=error)


# Interactive dashboard Routes

@app.route('/dashboard')
@login_required
def interactive_dashboard():
    csv_path = session.get(SESSION_CSV_KEY)
    if not csv_path or not os.path.exists(csv_path):
        return redirect(url_for('upload'))
    return render_template('dashboard.html')


@app.route('/api/cities')
@login_required
def api_cities():
    csv_path = session.get(SESSION_CSV_KEY)
    if not csv_path or not os.path.exists(csv_path):
        return jsonify({'error': 'No CSV uploaded.'}), 400
    try:
        data = load_weather_data(csv_path)
        cities = sorted({r['Location'] for r in data if r.get('Location')})
        return jsonify({'cities': cities})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chart')
@login_required
def api_chart():
    category = request.args.get('category', '').strip()
    city = request.args.get('city', '').strip()
    csv_path = session.get(SESSION_CSV_KEY)

    if not csv_path or not os.path.exists(csv_path):
        return jsonify({'error': 'No CSV uploaded.'}), 400
    if category not in ('temperature', 'rainfall', 'extreme'):
        return jsonify({'error': 'Invalid category.'}), 400
    if not city:
        return jsonify({'error': 'City is required.'}), 400

    try:
        all_data = load_weather_data(csv_path)
        city_data = list(filter_by_location(all_data, city))
        if not city_data:
            return jsonify({'error': f'No data found for city: {city}'}), 404
        charts, summary = _build_charts_and_summary(category, city, city_data)
        return jsonify({'charts': charts, 'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Existing Routes (protected)

@app.route('/')
@login_required
def index():
    data, locations = get_data()
    stats = _compute_overall_stats(data)
    rain_patterns = analyze_rain_patterns(data)
    recent_queries = QueryLog.query.order_by(QueryLog.timestamp.desc()).limit(5).all()
    return render_template(
        'index.html',
        stats=stats,
        rain_patterns=rain_patterns,
        locations=locations,
        location_count=len(locations),
        recent_queries=recent_queries,
    )


@app.route('/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
    data, locations = get_data()
    results = None
    result_stats = None
    form_values = {}

    if request.method == 'POST':
        location = request.form.get('location', '').strip() or None
        try:
            min_temp = float(request.form['min_temp']) if request.form.get('min_temp') else None
        except ValueError:
            min_temp = None
        try:
            max_temp = float(request.form['max_temp']) if request.form.get('max_temp') else None
        except ValueError:
            max_temp = None
        try:
            min_rainfall = float(request.form['min_rainfall']) if request.form.get('min_rainfall') else None
        except ValueError:
            min_rainfall = None
        rain_today = request.form.get('rain_today') or None

        form_values = {
            'location': location or '',
            'min_temp': request.form.get('min_temp', ''),
            'max_temp': request.form.get('max_temp', ''),
            'min_rainfall': request.form.get('min_rainfall', ''),
            'rain_today': request.form.get('rain_today', ''),
        }

        filtered = data
        if location:
            filtered = filter_by_location(filtered, location)
        if min_temp is not None:
            filtered = filter_high_temperature_days(filtered, min_temp)
        if max_temp is not None:
            filtered = [r for r in filtered
                        if r.get('MaxTemp') is not None and r['MaxTemp'] <= max_temp]
        if min_rainfall is not None:
            filtered = filter_by_rainfall_threshold(filtered, min_rainfall)
        if rain_today:
            filtered = [r for r in filtered if r.get('RainToday') == rain_today]

        results = filtered[:200]
        result_stats = _compute_overall_stats(filtered)

        entry = QueryLog(
            query_type='analysis',
            location=location,
            min_temp=min_temp,
            max_temp=max_temp,
            min_rainfall=min_rainfall,
            rain_today=rain_today,
            result_count=len(filtered),
        )
        db.session.add(entry)
        db.session.commit()

    return render_template(
        'analysis.html',
        locations=locations,
        results=results,
        result_stats=result_stats,
        form_values=form_values,
    )


@app.route('/locations')
@login_required
def locations():
    data, location_list = get_data()
    all_stats = []
    for loc in location_list:
        s = _get_or_cache_location_stats(loc, data)
        if s:
            all_stats.append(s)
    return render_template('locations.html', location_stats=all_stats)


@app.route('/location/<name>')
@login_required
def location_detail(name):
    data, locations = get_data()
    stats = _get_or_cache_location_stats(name, data)
    if not stats:
        return render_template('404.html', message=f'Location "{name}" not found.'), 404

    loc_data = filter_by_location(data, name)
    rain_patterns = analyze_rain_patterns(loc_data)

    entry = QueryLog(
        query_type='location',
        location=name,
        result_count=stats.total_records,
    )
    db.session.add(entry)
    db.session.commit()

    return render_template(
        'location_detail.html',
        location=name,
        stats=stats,
        rain_patterns=rain_patterns,
        locations=locations,
    )


@app.route('/visualizations')
@login_required
def visualizations():
    data, locations = get_data()
    if not _plots_exist():
        _generate_plots(data)
    return render_template('visualizations.html', plots=PLOT_DEFINITIONS)


@app.route('/visualizations/generate', methods=['POST'])
@login_required
def generate_visualizations():
    data, _ = get_data()
    _generate_plots(data)
    return redirect(url_for('visualizations'))


@app.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = QueryLog.query.order_by(QueryLog.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template('history.html', pagination=pagination)


@app.route('/prediction', methods=['GET', 'POST'])
@login_required
def prediction():
    model = get_model()
    prediction_result = None
    form_values = {}
    error = None

    if request.method == 'POST':
        feature_input = {}
        for col in FEATURE_COLUMNS:
            raw = request.form.get(col, '').strip()
            if col == 'RainToday_bin':
                feature_input[col] = int(raw) if raw in ('0', '1') else 0
            else:
                try:
                    feature_input[col] = float(raw) if raw else None
                except ValueError:
                    feature_input[col] = None

        try:
            prediction_result = predict_rain(model, feature_input)
        except Exception as e:
            error = str(e)

        entry = QueryLog(
            query_type='prediction',
            result_count=1 if prediction_result else 0,
        )
        db.session.add(entry)
        db.session.commit()

        form_values = {col: request.form.get(col, '') for col in FEATURE_COLUMNS}

    return render_template(
        'prediction.html',
        model=model,
        feature_columns=FEATURE_COLUMNS,
        prediction_result=prediction_result,
        form_values=form_values,
        error=error,
    )


# App startup

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('weather123')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
