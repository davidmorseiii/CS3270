# Weather App
A semester long weather app project for CS 3270.

## Description

### Module 10: Predictive Modeling with scikit learn
#### Machine learning rain prediction using scikit learn Pipelines.

* **Models:**
  * **Random Forest Classifier** — 100 estimators trained on 80% of all records shown with test set accuracy.
  * **Logistic Regression** — comparison model. Both accuracies displayed on the Predictions page.
* **Pipeline:** `SimpleImputer` (mean) > `StandardScaler` > classifier — handles columns with up to 48% missing values w/out dropping rows.
* **Features:** 17 weather measurements — temperature, humidity, pressure, wind speed, cloud cover, rainfall, and binary RainToday flag.
* **Page:** `/prediction` — displays model accuracy, ranked feature importance table, an interactive prediction form, and the predicted outcome with rain probability.

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
│   ├── prediction.py               # scikit-learn rain prediction models
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
│   ├── history.html                # Query history
│   └── prediction.html             # ML prediction page
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
