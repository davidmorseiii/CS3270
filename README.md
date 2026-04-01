# Weather App
A semester long weather app project for CS 3270.

## Description

### Module 9: 3 Tier Flask Web Application
#### Developed a browser based 3 tier web application using Flask, Jinja2, SQLite, and SQLAlchemy.

* **Three tier architecture:**
  * **UI**: Browser based HTML/CSS interface with Jinja2 templates. User can filter records, browse locations, view the visualizations, and see query history.
  * **Business Logic**: Flask routes and Python functions in `app.py` handle request processing, apply filters using my existing analysis modules and compute statistics on demand.
  * **Data Access**: SQLite database via SQLAlchemy (`models.py`) stores two types of application data:
    * **`QueryLog`** — analysis querys submitted through the UI.
    * **`LocationStats`** — per location stats computed once and cached so not recomputed on every request.

* **Pages:**
  * **Dashboard** (`/`) — Overall dataset statistics, rain pattern summary, and recent query history.
  * **Analysis** (`/analysis`) — Filter records by location, temp range, rainfall, and rain status. Shows matching statistics and a data table up to 200 rows.
  * **Locations** (`/locations`) — Table of all 49 locations with cached statistics.
  * **Location Detail** (`/location/<name>`) — Per location stats and rain patterns.
  * **Visualizations** (`/visualizations`) — All six matplotlib charts from `static/img/`. "Regenerate" button re runs plot generation.
  * **History** (`/history`) — Log of all queries stored in SQLite.

---
### Module 8: PySpark Distributed Processing
#### Implemented distributed data analysis with Apache PySpark on a 3 node cluster.

* New features incorporated:
  * **Distributed Analysis Functions**: Added `spark_analysis.py` with PySpark DataFrame equivilents of the main analysis functions.
  * **Spark Job Entry Point**: Created `spark_job.py` for submitting work to Spark cluster via `spark-submit`.

* Note: Module 9 does not require Spark and runs on a single machine.

---
#### Automated Tests List
* **Visualization Module**
  * `TestFilterFunctions`: `test_filter_rainfall_threshold`, `test_filter_high_temperature`, `test_filter_windy_days`, `test_filter_by_location`
  * `TestTransformFunctions`: `test_extract_temperature_range`, `test_extract_humidity_change`, `test_extract_pressure_change`
  * `TestAggregateFunctions`: `test_calculate_total_rainfall`, `test_find_max_temperature`, `test_find_min_temperature`

---
## Project Setup
- IDE: VS Code
- Environment: Ubuntu (I caved, shame on me. I started this project using Pycharm in Windows for the sake of learning something new, but as complexity grew, so did my frustration with Windows)
- Source Control: GitHub

---
## Requirements
- Python 3.8 or higher

---
## Getting Started

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
pip install flask flask-sqlalchemy
```

### 4. Run the original CLI analysis
```bash
python main.py
```

### 5. Run the Flask web application

```bash
python app.py
```

Then open: **http://127.0.0.1:5000** in your browser

The app will:
1. Load all weather records from `Weather Training Data.csv` on first request (takes a few seconds).
2. Create `weather_app.db` automatically in project root.
3. Generate the six visualization charts into `static/img/` on first visit to the visualizations page.

---
## Running the Tests
```bash
pytest test_weather_analysis.py -v
```

Include doctests:
```bash
pytest test_weather_analysis.py --doctest-modules -v
```

---
## Project Structure

```
CS3270/
├── app.py                          # Flask web application (entry point)
├── models.py                       # SQLAlchemy models (QueryLog, LocationStats)
├── main.py                         # Original CLI entry
├── spark_job.py                    # PySpark distributed job
├── test_weather_analysis.py        # pytest test suite
├── setup.py                        # Package configuration
├── weather_app.db                  # SQLite database (created on first run)
├── weather_analysis/               # Core analysis package
│   ├── analytics.py                # Statistical functions
│   ├── data_cleaning.py            # Data validation
│   ├── data_loader.py              # CSV loading (sync & async)
│   ├── logger_config.py            # Logging setup
│   ├── spark_analysis.py           # PySpark functions
│   ├── visualization.py            # Plotting & filter/map/reduce functions
│   └── weather_dataset.py          # WeatherDataset class
├── templates/                      # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html                  # Dashboard
│   ├── analysis.html               # Filter & query page
│   ├── locations.html              # Location list
│   ├── location_detail.html        # Per location detail
│   ├── visualizations.html         # Charts page
│   └── history.html                # Query history
├── static/
│   ├── css/style.css               # Stylesheet
│   └── img/                        # Generated plot images
└── AustraliaWeatherData/
    ├── Weather Training Data.csv   
    └── Weather Test Data.csv       
```

---
## Author
* Name: David Morse
* Email: dmmorse3@gmail.com
