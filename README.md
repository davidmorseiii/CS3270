# Weather App
A semester long weather app project for CS 3270.

---
## Description

### Module 5: Unit Testing
#### Added comprehensive unit tests to verify functionality of entire codebase.

* New features incorporated:
  * Unit Tests: Implemented a full set of tests covering all classes and methods.
  * Test Coverage: Verified logic for taking in csv data, generator processing, and statistical analysis.
* How they meet phase expectations:
  * Code Quality: Ensured reliability through testing of success and failure scenarios.
  * Regression Testing: Established good baseline to prevent future changes from breaking existing functionality.

#### Automated Tests List
* **Analytics**
  * `TestCalculateMean`: `test_mean_basic`, `test_mean_negative_values`, `test_mean_mixed_values`, `test_mean_empty_list`, `test_mean_with_iterator`
  * `TestCalculateMedian`: `test_median_odd_length`, `test_median_even_length`, `test_median_unsorted`, `test_median_empty_list`, `test_median_with_iterator`
  * `TestCalculateRange`: `test_range_basic`, `test_range_negative_values`, `test_range_mixed_values`, `test_range_empty_list`
  * `TestCalculateStatisticsStreaming`: `test_streaming_basic`, `test_streaming_empty_iterator`

* **Data Cleaning**
  * `TestValidNumericValuesGenerator`: `test_generator_basic`, `test_generator_filters_none`, `test_generator_filters_nan`, `test_generator_empty_data`, `test_generator_missing_column`
  * `TestExtractValidNumericValues`: `test_extract_basic`, `test_extract_with_invalid_values`
  * `TestFilterRowsByCondition`: `test_filter_basic`, `test_filter_none_match`, `test_filter_all_match`, `test_filter_non_callable`

* **Data Loading**
  * `TestCSVRowGenerator`: `test_csv_generator_basic`, `test_csv_generator_missing_file`, `test_csv_generator_empty_file`
  * `TestLoadWeatherData`: `test_load_basic`, `test_load_missing_file`

* **WeatherDataset**
  * `TestWeatherDataset`: `test_init_eager_loading`, `test_init_lazy_loading`, `test_get_row_count`, `test_get_column_statistics`, `test_get_column_statistics_with_none`, `test_get_data`, `test_iter_rows`, `test_missing_file`, `test_lazy_loading_triggers_on_access`
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