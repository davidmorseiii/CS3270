# Weather App
A semester long weather app project for CS 3270.

---
## Description

### Module 6: Data Patterns, Trends, Visualize
#### Analyzed weather data to identify patterns and trends with visualization using charts and graphs.

* New features incorporated:
  * **Functional Programming**: Used map, filter, lambda expressions, and reduce throughout the visualization module for data processing and analysis.
  * **Data Filtering**: Created functions to filter weather data for specific conditions (rainfall thresholds, high temperatures, windy days, locations) using filter() and lambda expressions.
  * **Data Transformation**: Implemented map() with lambda to extract derived metrics (temperature ranges, humidity changes, pressure changes).
  * **Data Aggregation**: Used reduce() with lambda to calculate totals and find extremes (total rainfall, max/min temps).
  * **Pattern Analysis**: Identified weather patterns including rain trends, temperature extremes, and correlations between variables.
  * **Visualizations Created**:
    * Temperature Distribution: Histogram showing frequency distribution of maximum temperatures across the dataset.
    * Rainfall Patterns: Histogram of rainfall amounts on rainy days to understand precipitation intensity.
    * Temperature vs Humidity: Scatter plot revealing relationship between temp and humidity levels.
    * Wind Speed Distribution: Histogram showing the distribution of wind gust speeds.
    * Pressure vs Rain: Box plot comparing atmospheric pressure on rainy vs non rainy days to identify weather patterns.
    * Temperature Range Trends: Histogram of daily temp ranges (MaxTemp - MinTemp) to understand temp variability.
* How they meet phase expectations:
  * **Map**: Used extensively to transform data (extract values, calculate derived metrics like temperature ranges).
  * **Filter**: Applied throughout to select data subsets (high temps, heavy rain, windy conditions) using lambda predicates.
  * **Lambda**: Integrated in all filtering and mapping operations for concise, functional data processing.
  * **Reduce**: Implemented for aggregations (sum rainfall, find max/min temps) with lambda functions.
  * **Visualization Libraries**: Used matplotlib for plotting, demonstrating data patterns through 6 different chart types.
  * **Pattern Discovery**: Identified meaningful weather patterns (rain probability, temperature extremes, pressure rain correlation).

#### Automated Tests List
* **Visualization Module**
  * `TestFilterFunctions`: `test_filter_rainfall_threshold`, `test_filter_high_temperature`, `test_filter_windy_days`, `test_filter_by_location`
  * `TestTransformFunctions`: `test_extract_temperature_range`, `test_extract_humidity_change`, `test_extract_pressure_change`
  * `TestAggregateFunctions`: `test_calculate_total_rainfall`, `test_find_max_temperature`, `test_find_min_temperature`

---
## Project Setup
- IDE: PyCharm Professional
- Environment: Windows 11
- Source Control: GitHub
- Notes: I have been using Linux with VS Code to program for several years now, and I realized that I'm not nearly as comfortable on Windows as I want to be.
  I'm choosing to work on Windows and try a new IDE this semester to strengthen my confidence with Windows and learn something new.

---
## Requirements
- Python 3.8 or higher

---
## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/davidmorseiii/CS3270.git
```

### 2. Navigate to the project directory
```bash
cd CS3270
```

### 3. Create a virtual environment (recommended)

#### On MacOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
#### On Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

### 4. Install the package
```bash
pip install .
```

### 5. Run the program
```bash
python main.py
```
---
## Author
* Name: David Morse
* Email: dmmorse3@gmail.com