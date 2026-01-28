# Weather App
A semester long weather app project for CS 3270.

---
## Description

### Phase 3: OOP
#### Fetches weather data from CSV, cleans it, and calculates descriptive statistics using an object oriented approach.

* New features incorporated:
  * Object-Oriented Programming: Implemented a `WeatherDataset` class to encapsulate weather data and related operations.
  * Encapsulation: The class manages its own data loading and provides methods (`get_column_statistics`) to access results and hide implementation details.
* How they meet phase expectations:
  * OOP Implementation: The project now uses a class based approach where the data and statistics calculations are combined into a single entity.
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