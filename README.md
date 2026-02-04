# Weather App
A semester long weather app project for CS 3270.

---
## Description

### Module 4: Generators and Iterators
#### Fetches weather data from CSV, processes it using generators/iterators for memory efficiency, and calculates descriptive statistics with comprehensive error handling and logging.

* New features incorporated:
  * Generators & Iterators: Implemented memory efficient data processing with `csv_row_generator()`, `valid_numeric_values_generator()`, and `iter_rows()` methods that process data on demand.
  * Robust Error Handling: Added comprehensive exception handling throughout with specific error types (FileNotFoundError, PermissionError, ValueError, TypeError, csv.Error).
  * File Handling: Created `open_csv_file()` context manager to ensure proper file opening and closing even when errors occur.
  * Logging System: Implemented centralized logging configuration with rotating file handlers (10MB max, 5 backups) that log to both console and individual module log files.
  * Lazy Loading: Added `lazy_load` option parameter to `WeatherDataset` class for on demand data loading.
  * Streaming Statistics: Added `calculate_statistics_streaming()` for single pass statistics calculation on large datasets
* How they meet phase expectations:
  * Generators/Iterators: Data is processed incrementally using generators, reducing memory for large CSV files.
  * Error Handling: Every module now includes try except blocks with specific exception types and graceful degradation.
  * Logging: All operations are logged to both console and rotating log files in the `logs/` directory.
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