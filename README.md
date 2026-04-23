# Weather Analysis App

A semester long weather analytics web application for CS 3270, built with Flask and Python. Analyzes Australian weather data with interactive visualizations, machine learning rain prediction, and authenticated user interface.

---

## Features

- **User Authentication** — Secure login screen using Flask-Login and hashed passwords (werkzeug `pbkdf2:sha256`). Routes are protected. Unauthenticated requests redirect to `/login`.
- **CSV Upload** — After login, upload any Australian weather CSV file. The uploaded dataset powers the interactive dashboard analysis.
- **Interactive Dashboard** — Single page dashboard with three weather category buttons: dynamic city dropdown, AJAX powered charts, and summaries without any page reloads.
- **Analysis & Filtering** — Filter records by location, temperature range, rainfall, and rain indicator.
- **Locations** — Browse per city statistics cached in SQLite for fast repeated access.
- **Visualizations** — Six pregenerated matplotlib charts saved to disk.
- **Query History** — Paginated log of all analysis queries.
- **Rain Prediction** — Machine learning models (Random Forest + Logistic Regression) with scikit-learn to predict next day rainfall.
- **PySpark** — Optional distributed analytics support via `spark_job.py`.

---

## System Architecture

```
Browser
  │  HTTP (form posts, AJAX fetch)
  ▼
Flask app (app.py)
  ├── Flask-Login — session-based auth, @login_required on all routes
  ├── Upload route — saves CSV to uploads/, stores path in session
  ├── API routes (/api/cities, /api/chart) — JSON responses for AJAX
  ├── Existing routes (/, /analysis, /locations, /visualizations, /history, /prediction)
  │
  ├── weather_analysis/ package
  │     ├── data_loader.py    — CSV parsing (sync and async)
  │     ├── analytics.py      — mean, median, range, streaming stats
  │     ├── data_cleaning.py  — generators and validators
  │     ├── visualization.py  — matplotlib plots, filter/map/reduce
  │     ├── prediction.py     — scikit-learn ML pipeline
  │     └── spark_analysis.py — PySpark distributed functions
  │
  └── SQLite (weather_app.db)
        ├── user         — authentication (hashed passwords)
        ├── query_log    — history of all user queries
        └── location_stats — cached per city statistics
```

### Dashboard Flow

1. User logs in > redirected to `/upload`
2. User uploads a `.csv` file > validated (required columns + non empty), saved to `uploads/` folder, path stored in session
3. Redirected to `/dashboard` (SPA shell)
4. User clicks a category button > JS calls `GET /api/cities` > dropdown populated from uploaded CSV
5. User selects a city > JS calls `GET /api/chart?category=X&city=Y` > server returns base64 encoded matplotlib PNGs + a text summary
6. JS injects charts and summary into the page — no page reload

---

## CSV Upload

- **Accepted format:** `.csv` files only, maximum 50 MB
- **Required columns:** `Location`, `MinTemp`, `MaxTemp`, `Rainfall`, `RainToday`
- Additional columns (humidity, wind speed, pressure, etc.) are used for visualizations if present
- The standard `Weather Training Data.csv` in `AustraliaWeatherData/` are fully compatible
- Each user session maintains its own uploaded file where uploading again replaces the previous file

---

## Interactive Dashboard

### Category Buttons

| Button | Category Value | Charts Generated | Summary Includes |
|---|---|---|---|
| Temperature Trends | `temperature` | Histogram of MaxTemp, Histogram of MinTemp | Avg max/min, record high/low |
| Rainfall Patterns | `rainfall` | Histogram of rainy day rainfall, Rainy vs Dry day bar chart | Total rainfall, % rainy days, avg rainfall on rainy days |
| Extreme Weather | `extreme` | Wind gust speed histogram, MaxTemp vs WindGustSpeed scatter | Extreme heat days (>35°C), high-wind days (>60 km/h) |

### AJAX Behavior

- Clicking category button fetches `GET /api/cities` > populates city dropdown
- Changing the city selection fetches `GET /api/chart?category=X&city=Y` > renders PNG charts (base64) and a text summary panel
- A loading spinner displays during fetch. Errors are shown inline
- All interactions happen without navigating to different page

---

## Security

- Passwords are hashed with `werkzeug.security.generate_password_hash` (PBKDF2 + SHA-256 + salt)
- Flask-Login manages session cookies signed with `SECRET_KEY`
- Every route except `/login` requires authentication via `@login_required`
- Uploaded files are validated for extension, size, and required columns before being saved
- Uploaded files are stored in server side `uploads/` directory (not served as static assets)
- Sessions store only file path (not file contents)

---

## Project Setup

### Requirements

- Python 3.8 or higher
- pip

### 1. Clone the repository

```bash
git clone https://github.com/davidmorseiii/CS3270.git
cd CS3270
```

### 2. Create and activate a virtual environment

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install .
```

### 4. Run the Flask web application

```bash
python3 app.py
```

Then open **http://127.0.0.1:5000** in your browser.

**Default login credentials:**
- Username: `admin`
- Password: `password123`

The app will:
1. Create `weather_app.db` and seed the default admin user on first run.
2. Load weather records from `Weather Training Data.csv` on first authenticated request.
3. Generate visualization charts into `static/img/` on first visit to Visualizations page.

### 5. Run the original CLI analysis (optional)

```bash
python3 main.py
```

---

## Running the Tests

```bash
pytest test_weather_analysis.py -v
```

Include doctests:
```bash
pytest test_weather_analysis.py --doctest-modules -v
```

### Test Coverage

| Class | Tests |
|---|---|
| `TestCalculateMean` | Basic, negative, mixed, empty, iterator inputs |
| `TestCalculateMedian` | Odd/even length, unsorted, empty, iterator |
| `TestCalculateRange` | Basic range calculation |
| `TestStatisticsStreaming` | Single pass streaming statistics |
| `TestFilterFunctions` | rainfall threshold, high temperature, windy days, by location |
| `TestTransformFunctions` | temperature range, humidity change, pressure change |
| `TestAggregateFunctions` | total rainfall, max temp, min temp |
| `TestAuthLogic` | Password hashing, valid/invalid login, route protection, logout |
| `TestCSVUploadValidation` | Valid upload, missing columns, empty CSV, wrong extension, no file |
| `TestDashboardAPI` | Cities endpoint, chart endpoint for all 3 categories, error cases |

---

## Project Structure

```
CS3270/
├── app.py                          # Flask web application (entry point)
├── models.py                       # SQLAlchemy models (User, QueryLog, LocationStats)
├── main.py                         # Original CLI entry
├── spark_job.py                    # PySpark distributed job
├── test_weather_analysis.py        # pytest test suite
├── setup.py                        # Package configuration
├── weather_app.db                  # SQLite database (created on first run)
├── uploads/                        # Per session uploaded CSV files (gitignored)
├── weather_analysis/               # Core analysis package
│   ├── analytics.py                # Statistical functions (mean, median, range)
│   ├── data_cleaning.py            # Data validation and generators
│   ├── data_loader.py              # CSV loading (sync & async)
│   ├── logger_config.py            # Logging setup with file rotation
│   ├── prediction.py               # scikit-learn rain prediction models
│   ├── spark_analysis.py           # PySpark distributed functions
│   ├── visualization.py            # Matplotlib plots, filter/map/reduce
│   └── weather_dataset.py          # WeatherDataset class (lazy/eager)
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                   # Navbar and layout base
│   ├── login.html                  # Standalone login form
│   ├── upload.html                 # CSV upload page
│   ├── dashboard.html              # Interactive SPA dashboard
│   ├── index.html                  # Overview dashboard
│   ├── analysis.html               # Filter & query page
│   ├── locations.html              # Location list
│   ├── location_detail.html        # Per location detail
│   ├── visualizations.html         # Static charts page
│   ├── history.html                # Query history
│   └── prediction.html             # ML prediction page
├── static/
│   ├── css/style.css               # Dark themed stylesheet
│   ├── js/dashboard.js             # Vanilla JS AJAX
│   └── img/                        # Generated static plot images
└── AustraliaWeatherData/
    ├── Weather Training Data.csv
    └── Weather Test Data.csv
```

---

## Development Phases

### Module 1–5: Core Analysis
`weather_analysis/` package with CSV loading, statistical functions, data cleaning generators, and functional programming patterns (map/filter/reduce).

### Module 6–7: Visualization & Async
matplotlib plotting functions and async CSV loading with `asyncio`. Multiprocessing for parallel chart generation.

### Module 8–9: Flask Web App
Migrated from CLI to Flask web application with Jinja2, SQLAlchemy models for query logging and location statistics caching, and responsive UI.

### Module 10: Machine Learning
scikit-learn pipelines (RandomForest + LogisticRegression) with `SimpleImputer` and `StandardScaler` preprocessing, handling up to 48% missing values. The `/prediction` route exposes interactive form with feature importance ranking.

### Module 11: Authentication, Upload & Interactive Dashboard
Added Flask-Login for session based authentication with hashed passwords. Built CSV upload flow so users can supply their own dataset. Built a single page interactive dashboard with three weather category buttons, an AJAX-powered city dropdown, and dynamically rendered matplotlib charts w/ text summaries. Comprehensive test coverage for auth, upload validation, and the dashboard API.

---

## Author

- **Name:** David Morse
- **Email:** dmmorse3@gmail.com
- **GitHub:** https://github.com/davidmorseiii/CS3270
