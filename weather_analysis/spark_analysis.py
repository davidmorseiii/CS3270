from typing import Dict
from pyspark.sql import DataFrame
import pyspark.sql.functions as F


def total_rainfall_df(df: DataFrame) -> float:
    """Distributed total rainfall (ignores nulls). Returns 0.0 when no data."""
    res = df.agg(F.sum(F.col('Rainfall')).alias('total')).first()
    total = res['total'] if res is not None else None
    return float(total) if total is not None else 0.0


def max_temperature_df(df: DataFrame) -> float:
    """Distributed max of `MaxTemp`. Returns None when unavailable."""
    res = df.agg(F.max(F.col('MaxTemp')).alias('max')).first()
    return res['max'] if res is not None else None


def min_temperature_df(df: DataFrame) -> float:
    """Distributed min of `MinTemp`. Returns None when unavailable."""
    res = df.agg(F.min(F.col('MinTemp')).alias('min')).first()
    return res['min'] if res is not None else None


def count_rainy_days_df(df: DataFrame) -> int:
    """Count rows where `RainToday` == 'Yes' in a distributed manner."""
    return int(df.filter(F.col('RainToday') == 'Yes').count())


def analyze_rain_patterns_df(df: DataFrame) -> Dict[str, int]:
    """Return rain pattern aggregates computed with a single aggregation call."""
    agg = df.select(
        F.sum(F.when(F.col('RainToday') == 'Yes', 1).otherwise(0)).alias('rain_today'),
        F.sum(F.when(F.col('RainTomorrow') == 'Yes', 1).otherwise(0)).alias('rain_tomorrow'),
        F.sum(F.when((F.col('RainToday') == 'Yes') & (F.col('RainTomorrow') == 'Yes'), 1).otherwise(0)).alias('consecutive_rain'),
        F.count(F.lit(1)).alias('total_days')
    ).first()

    return {
        'rain_today': int(agg['rain_today'] or 0),
        'rain_tomorrow': int(agg['rain_tomorrow'] or 0),
        'consecutive_rain': int(agg['consecutive_rain'] or 0),
        'total_days': int(agg['total_days'] or 0),
    }


def temperature_range_stats_df(df: DataFrame) -> Dict[str, float]:
    """Compute average, max, min of daily (MaxTemp - MinTemp) where both are present."""
    range_col = (F.col('MaxTemp') - F.col('MinTemp')).alias('range')
    filtered = df.select(range_col).filter(F.col('range').isNotNull())
    if filtered.rdd.isEmpty():
        return {'avg': None, 'max': None, 'min': None, 'count': 0}

    agg = filtered.agg(
        F.avg(F.col('range')).alias('avg'),
        F.max(F.col('range')).alias('max'),
        F.min(F.col('range')).alias('min'),
        F.count(F.col('range')).alias('count')
    ).first()

    return {
        'avg': float(agg['avg']) if agg['avg'] is not None else None,
        'max': float(agg['max']) if agg['max'] is not None else None,
        'min': float(agg['min']) if agg['min'] is not None else None,
        'count': int(agg['count']) if agg['count'] is not None else 0,
    }
