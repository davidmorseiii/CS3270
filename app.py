import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from models import db, QueryLog, LocationStats
from weather_analysis import (
    load_weather_data,
    filter_by_rainfall_threshold,
    filter_high_temperature_days,
    filter_by_location,
    analyze_rain_patterns,
    find_max_temperature,
    find_min_temperature,
    calculate_total_rainfall,
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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "weather_app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'weather-analysis-cs3270'

db.init_app(app)

# Data loading: once at startup, then held in moudle level variable
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
    """Return mean of a list of floats, or none if empty."""
    valid = [v for v in values if v is not None and isinstance(v, (int, float))]
    return round(sum(valid) / len(valid), 2) if valid else None


def _compute_overall_stats(data):
    """Compute summary statistics for full or filtreed dataset"""
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


# Routes

@app.route('/')
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

        # apply filters incrementaly
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

        results = filtered[:200]  # cap display rows to keep page responsive
        result_stats = _compute_overall_stats(filtered)

        # log the query
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
def locations():
    data, location_list = get_data()
    all_stats = []
    for loc in location_list:
        s = _get_or_cache_location_stats(loc, data)
        if s:
            all_stats.append(s)
    return render_template('locations.html', location_stats=all_stats)


@app.route('/location/<name>')
def location_detail(name):
    data, locations = get_data()
    stats = _get_or_cache_location_stats(name, data)
    if not stats:
        return render_template('404.html', message=f'Location "{name}" not found.'), 404

    loc_data = filter_by_location(data, name)
    rain_patterns = analyze_rain_patterns(loc_data)

    # log the query
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
def visualizations():
    data, locations = get_data()
    if not _plots_exist():
        _generate_plots(data)
    return render_template('visualizations.html', plots=PLOT_DEFINITIONS)


@app.route('/visualizations/generate', methods=['POST'])
def generate_visualizations():
    data, _ = get_data()
    _generate_plots(data)
    return redirect(url_for('visualizations'))


@app.route('/history')
def history():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = QueryLog.query.order_by(QueryLog.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template('history.html', pagination=pagination)


@app.route('/prediction', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
