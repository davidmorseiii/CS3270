#!/usr/bin/env python3
"""Reads the CSV using Spark, converts rows to plain Python dicts and reuses the existing analysis/visualization function. Designed to run with spark-submit cluster or local mode."""
from __future__ import annotations
import argparse
from pyspark.sql import SparkSession
from weather_analysis.logger_config import setup_logger
from weather_analysis import (
    filter_by_rainfall_threshold,
    filter_high_temperature_days,
    filter_windy_days,
    calculate_total_rainfall,
    find_max_temperature,
    find_min_temperature,
    count_rainy_days,
    analyze_rain_patterns,
    extract_temperature_range,
    generate_all_plots_parallel,
    # distributed variants
    total_rainfall_df,
    max_temperature_df,
    min_temperature_df,
    count_rainy_days_df,
    analyze_rain_patterns_df,
    temperature_range_stats_df,
)

logger = setup_logger('spark_job')


def row_to_py(row) -> dict:
    """Convert pyspark Row to a plain Python dict with primitive types."""
    d = row.asDict(recursive=True)
    for k, v in list(d.items()):
        # keep None as is
        if v is None:
            continue
        # PySpark already uses python numeric types when inferSchema=True
        # but sometimes values arrive as strings. coerce to float when possible
        if isinstance(v, str):
            try:
                # preserve integer vs float where reasonable
                if v.isdigit():
                    d[k] = int(v)
                else:
                    d[k] = float(v)
            except Exception:
                d[k] = v
        else:
            d[k] = v
    return d


def run(file_path: str):
    logger.info(f"Starting Spark job for: {file_path}")

    spark = SparkSession.builder.appName("WeatherAnalysisSpark").getOrCreate()

    # read CSV with header and attempt to infer schema
    df = spark.read.option("header", "true").option("inferSchema", "true").csv(file_path)
    logger.info(f"Read CSV as Spark DataFrame with {df.count()} rows and {len(df.columns)} columns")

    print("=" * 60)
    print("WEATHER DATA ANALYSIS (Spark - distributed where possible)")
    print("=" * 60)

    print("\n-- Rain Pattern Analysis (distributed) --")
    rain_patterns = analyze_rain_patterns_df(df)
    print(rain_patterns)

    print("\n-- Temperature Extremes (distributed) --")
    max_temp = max_temperature_df(df)
    min_temp = min_temperature_df(df)
    print(f"Highest recorded temp: {max_temp}")
    print(f"Lowest recorded temp:  {min_temp}")

    print("\n-- Total Rainfall (distributed) --")
    total_rainfall = total_rainfall_df(df)
    print(f"Total rainfall: {total_rainfall:.1f} mm")

    print("\n-- Example Filters (driver-side) --")
    # for filter based lists and plotting still collect reasonable sized sample
    sample_data = df.limit(10000).rdd.map(row_to_py).collect()
    hot_days = filter_high_temperature_days(sample_data, 35.0)
    print(f"Sample: Days with MaxTemp >= 35°C: {len(hot_days)}")

    heavy_rain_days = filter_by_rainfall_threshold(sample_data, 10.0)
    print(f"Sample: Days with Rainfall >= 10mm: {len(heavy_rain_days)}")

    windy_days = filter_windy_days(sample_data, 60.0)
    print(f"Sample: Days with WindGust >= 60 km/h: {len(windy_days)}")

    print("\n-- Temperature Range Summary (distributed) --")
    tr_stats = temperature_range_stats_df(df)
    if tr_stats['count']:
        print(f"Average daily range: {tr_stats['avg']:.2f}°C (n={tr_stats['count']})")

    print("\n-- Generating Visualizations (parallel on driver, sampled) --")
    results = generate_all_plots_parallel(sample_data)
    for output_path, success in results:
        print(f"{output_path}: {'OK' if success else 'FAILED'}")

    spark.stop()
    logger.info("Spark job finished")


def main():
    parser = argparse.ArgumentParser(description="Run weather analysis using PySpark")
    parser.add_argument("file", help="Path to weather CSV file (HDFS, S3 or local)")
    args = parser.parse_args()
    run(args.file)


if __name__ == '__main__':
    main()
