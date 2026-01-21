# Weather App
A semester long weather app project for CS 3270.

---
## Description

### Phase 2: Modularization
#### Fetches weather data from CSV, cleans it, and calculates descriptive statistics using a modular architecture.

* New features incorporated:
  * Modularization: Split the code into a structured Python package (weather_analysis) with separate modules for input/output (load_csv_to_df.py), math (analytics.py), and data formatting (data_cleaning.py).
  * Descriptive Statistics: Added functions to calculate mean, median, and range of weather min and max temps.
  * Packaging: Created a setup.py file to allow the code to be installed via pip.
  * Reusability: With analysis logic decoupled from the data loading, the stats functions can work with any list of numbers.
* How they meet phase expectations:
  * Descriptive Stats: The analytics.py module explicitly handles calculation of several of the suggested statistics.
  * Install and Use: The project can now be installed using pip install . and imported into other scripts using standard import statements.
---
## Project Setup
- IDE: PyCharm Professional
- Environment: Windows 11
- Source Control: GitHub
- Notes: I have been using Linux with VS Code to program for several years now and I realized that I'm not nearly as comfortable in Windows as I want to be.
  I'm choosing to work in Windows and try a new IDE this semester to strengthen my confidence in Windows and learn something new.

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