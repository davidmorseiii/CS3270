# Migrating and Deploying Weather Analysis to PySpark

## Summary of changes
- Added `spark_job.py`: a Spark entrypoint that reads the CSV using `SparkSession`, converts rows to plain Python `dict`s, and reuses the existing analysis and plotting functions from `weather_analysis` package.

## Key considerations

- Data size and collection: Collecting the entire dataset to the driver is only appropriate for small to medium datasets. For large datasets best to refactor the analysis to use Spark DataFrame to avoid driver memory pressure.

- Schema inference: `spark_job.py` uses `option("inferSchema","true")` to get numeric column types automatically.

- Dependencies: The runtime must include `pyspark` (and `py4j`). In many production clusters `pyspark` is provided by the environment. For local testing, install `pyspark` via pip.

- Logging: The existing `logger_config` is reused by the Spark job. Spark executor logs remain managed by Spark, while driver-side logs go through the package logger.

## Files added

- `spark_job.py`
- `spark_analysis.py`

## Running locally with spark-submit

1. For local testing you can install:

```bash
pip install pyspark
```

2. Run the job with `spark-submit`. Ex: (local mode, 4 cores):

```bash
spark-submit --master local[4] spark_job.py "AustraliaWeatherData/Weather Training Data.csv"
``'