# Weather App
A semester long weather app project for CS 3270.

---
## Description

### Module 7: Multithreading Concurrency
#### Implemented asynchronous data fetching and multiprocessing for improved performance and efficiency.

* New features incorporated:
  * **Asynchronous Data Loading**: Implemented `load_weather_data_async()` in `data_loader.py` using Python's `asyncio` library to perform non blocking I/O operations when loading CSV files. This prevents the application from blocking on I/O bound tasks.
  * **Multiprocessing for Visualizations**: Added `generate_all_plots_parallel()` in `visualization.py` that uses Python's `multiprocessing.Pool` to generate all six visualization plots concurrently across multiple CPU cores. This significantly reduces the time required for intensive matplotlib rendering.
  * **Async Main Function**: Refactored `main.py` to use `async def async_main()` and `asyncio.run()` to support asynchronous execution flow.
  * **Non-Interactive Backend**: Configured matplotlib to use the 'Agg' backend for thread safe, non interactive plot generation suitable for multiprocessing.

* Where and why these features are used:
  * **Asyncio (data_loader.py)**: Used `asyncio` with `run_in_executor()` to offload file I/O operations to a thread pool, allowing event loop to remain responsive. This is ideal for I/O-bound tasks like reading large CSV files.
  * **Multiprocessing (visualization.py)**: Used `multiprocessing.Pool` to distribute the generation of 6 different visualization plots across multiple CPU cores. Each plot generation involves compute intensive operations (data filtering, statistical calculations, and matplotlib rendering), making it ideal for parallelism to utilize multi core CPUs.
  * **Why Async for I/O**: File reading is I/O-bound, meaning the CPU spends time waiting for disk operations. Async I/O allows other operations to go while waiting, improving overall application responsiveness.
  * **Why Multiprocessing for Plots**: Generating matplotlib visualizations is CPU intensive (data processing, rendering graphics). Multiprocessing bypasses Python's GIL to achieve true parallelism on multi core systems, which significantly reduces total execution time.

* Performance benefits:
  * Visualization generation time reduced by utilizing multiple CPU cores simultaneously
  * Same results as sequential version, only faster
  * Better resource utilization on multi-core systems

---

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