from functools import reduce
from typing import Iterable, Callable, List, Dict, Tuple
import matplotlib.pyplot as plt
from .logger_config import setup_logger

logger = setup_logger(__name__)


# -- Data Filtering Lambda and Filter --

def filter_by_rainfall_threshold(data: Iterable[dict], threshold: float) -> List[dict]:
    """
    Filter rows where rainfall exceeds threshold using filter and lambda
    Args:
        data: Iterable of weather data dicts
        threshold: Min rainfall value
    Returns:
        List of rows with rainfall >= threshold
    """
    logger.info(f"Filtering data for rainfall >= {threshold}")
    result = list(filter(
        lambda row: row.get('Rainfall') is not None
                    and isinstance(row['Rainfall'], (int, float))
                    and row['Rainfall'] >= threshold,
        data
    ))
    logger.info(f"Found {len(result)} rows with rainfall >= {threshold}")
    return result


def filter_high_temperature_days(data: Iterable[dict], temp_threshold: float) -> List[dict]:
    """
    Filter days with high max temp using filter and lambda
    Args:
        data: Iterable of weather data dicts
        temp_threshold: Min MaxTemp value
    Returns:
        List of rows with MaxTemp >= temp_threshold
    """
    logger.info(f"Filtering data for MaxTemp >= {temp_threshold}")
    result = list(filter(
        lambda row: row.get('MaxTemp') is not None
                    and isinstance(row['MaxTemp'], (int, float))
                    and row['MaxTemp'] >= temp_threshold,
        data
    ))
    logger.info(f"Found {len(result)} rows with MaxTemp >= {temp_threshold}")
    return result


def filter_windy_days(data: Iterable[dict], wind_speed_threshold: float) -> List[dict]:
    """
    Filter days with high wind gusts using filter and lambda
    Args:
        data: Iterable of weather data dicts
        wind_speed_threshold: Min WindGustSpeed value
    Returns:
        List of rows with WindGustSpeed >= wind_speed_threshold
    """
    logger.info(f"Filtering data for WindGustSpeed >= {wind_speed_threshold}")
    result = list(filter(
        lambda row: row.get('WindGustSpeed') is not None
                    and isinstance(row['WindGustSpeed'], (int, float))
                    and row['WindGustSpeed'] >= wind_speed_threshold,
        data
    ))
    logger.info(f"Found {len(result)} rows with WindGustSpeed >= {wind_speed_threshold}")
    return result


def filter_by_location(data: Iterable[dict], location: str) -> List[dict]:
    """
    Filter data for specific location using filter and lambda
    Args:
        data: Iterable of weather data dicts
        location: Location name to filter
    Returns:
        List of rows for specified location
    """
    logger.info(f"Filtering data for location: {location}")
    result = list(filter(lambda row: row.get('Location') == location, data))
    logger.info(f"Found {len(result)} rows for location: {location}")
    return result


# -- Data Transformation Map and Lambda --

def extract_temperature_range(data: Iterable[dict]) -> List[float]:
    """
    Calculate temperature range (MaxTemp - MinTemp) for each day using map and lambda
    Args:
        data: Iterable of weather data dicts
    Returns:
        List of temp ranges
    """
    logger.info("Calculating temperature ranges")
    result = list(map(
        lambda row: row['MaxTemp'] - row['MinTemp']
        if row.get('MaxTemp') is not None and row.get('MinTemp') is not None
        else None,
        data
    ))
    # filter out None values
    result = list(filter(lambda x: x is not None, result))
    logger.info(f"Calculated {len(result)} temperature ranges")
    return result


def extract_humidity_change(data: Iterable[dict]) -> List[float]:
    """
    Calculate humidity change from 9am - 3pm using map and lambda
    Args:
        data: Iterable of weather data dicts
    Returns:
        List of humidity changes
    """
    logger.info("Calculating humidity changes")
    result = list(map(
        lambda row: row['Humidity3pm'] - row['Humidity9am']
        if row.get('Humidity3pm') is not None and row.get('Humidity9am') is not None
        else None,
        data
    ))
    # filter out None values
    result = list(filter(lambda x: x is not None, result))
    logger.info(f"Calculated {len(result)} humidity changes")
    return result


def extract_pressure_change(data: Iterable[dict]) -> List[float]:
    """
    Calculate pressure change from 9am - 3pm using map and lambda
    Args:
        data: Iterable of weather data dicts
    Returns:
        List of pressure changes
    """
    logger.info("Calculating pressure changes")
    result = list(map(
        lambda row: row['Pressure3pm'] - row['Pressure9am']
        if row.get('Pressure3pm') is not None and row.get('Pressure9am') is not None
        else None,
        data
    ))
    # filter out None values
    result = list(filter(lambda x: x is not None, result))
    logger.info(f"Calculated {len(result)} pressure changes")
    return result


# -- Aggregation Functions with Reduce --

def calculate_total_rainfall(data: Iterable[dict]) -> float:
    """
    Calculate total rainfall across all days using reduce and lambda
    Args:
        data: Iterable of weather data dicts
    Returns:
        Total rainfall sum
    """
    logger.info("Calculating total rainfall using reduce")
    # extract rainfall values
    rainfall_values = list(filter(
        lambda x: x is not None,
        map(lambda row: row.get('Rainfall') if isinstance(row.get('Rainfall'), (int, float)) else None, data)
    ))

    if not rainfall_values:
        logger.warning("No valid rainfall values found")
        return 0.0

    total = reduce(lambda acc, val: acc + val, rainfall_values, 0.0)
    logger.info(f"Total rainfall: {total:.2f}")
    return total


def find_max_temperature(data: Iterable[dict]) -> float:
    """
    Find the max temp across all days using reduce and lambda
    Args:
        data: Iterable of weather data dicts
    Returns:
        Max temp
    """
    logger.info("Finding max temperature using reduce")
    # extract max temp values
    temp_values = list(filter(
        lambda x: x is not None,
        map(lambda row: row.get('MaxTemp') if isinstance(row.get('MaxTemp'), (int, float)) else None, data)
    ))

    if not temp_values:
        logger.warning("No valid temperature values found")
        return float('-inf')

    max_temp = reduce(lambda acc, val: max(acc, val), temp_values, float('-inf'))
    logger.info(f"Max temperature found: {max_temp:.2f}")
    return max_temp


def find_min_temperature(data: Iterable[dict]) -> float:
    """
    Find the min temp across all days using reduce and lambda
    Args:
        data: Iterable of weather data dicts
    Returns:
        Min temp
    """
    logger.info("Finding min temperature using reduce")
    # extract min temp values
    temp_values = list(filter(
        lambda x: x is not None,
        map(lambda row: row.get('MinTemp') if isinstance(row.get('MinTemp'), (int, float)) else None, data)
    ))

    if not temp_values:
        logger.warning("No valid temperature values found")
        return float('inf')

    min_temp = reduce(lambda acc, val: min(acc, val), temp_values, float('inf'))
    logger.info(f"Min temperature found: {min_temp:.2f}")
    return min_temp


# -- Pattern Analysis --

def count_rainy_days(data: Iterable[dict]) -> int:
    """
    Count days where it rained using filter and lambda
    Args:
        data: Iterable of weather data dicts
    Returns:
        Num of rainy days
    """
    logger.info("Counting rainy days")
    rainy = list(filter(lambda row: row.get('RainToday') == 'Yes', data))
    count = len(rainy)
    logger.info(f"Found {count} rainy days")
    return count


def analyze_rain_patterns(data: Iterable[dict]) -> Dict[str, int]:
    """
    Analyze rain patterns using functional programming
    Args:
        data: Iterable of weather data dicts
    Returns:
        Dict with rain pattern statistics
    """
    logger.info("Analyzing rain patterns")
    data_list = list(data)

    # count rain today
    rain_today_count = len(list(filter(lambda row: row.get('RainToday') == 'Yes', data_list)))

    # count rain tomorrow
    rain_tomorrow_count = len(list(filter(lambda row: row.get('RainTomorrow') == 'Yes', data_list)))

    # count consecutive rain (today and tomorrow)
    consecutive_rain = len(list(filter(
        lambda row: row.get('RainToday') == 'Yes' and row.get('RainTomorrow') == 'Yes',
        data_list
    )))

    result = {
        'rain_today': rain_today_count,
        'rain_tomorrow': rain_tomorrow_count,
        'consecutive_rain': consecutive_rain,
        'total_days': len(data_list)
    }

    logger.info(f"Rain pattern analysis: {result}")
    return result


# -- Visualization --

def plot_temperature_distribution(data: Iterable[dict], output_path: str = 'temperature_distribution.png'):
    """
    Create histogram of temp distribution using filtered data
    Args:
        data: Iterable of weather data dicts
        output_path: Path to save the plot
    """
    logger.info("Creating temperature distribution plot")

    # use map and filter to extract valid temp values
    max_temps = list(filter(
        lambda x: x is not None,
        map(lambda row: row.get('MaxTemp') if isinstance(row.get('MaxTemp'), (int, float)) else None, data)
    ))

    if not max_temps:
        logger.warning("No valid temperature data to plot")
        return

    plt.figure(figsize=(10, 6))
    plt.hist(max_temps, bins=50, edgecolor='black', alpha=0.7)
    plt.xlabel('Maximum Temperature (°C)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Maximum Temperatures')
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Temperature distribution plot saved to {output_path}")


def plot_rainfall_patterns(data: Iterable[dict], output_path: str = 'rainfall_patterns.png'):
    """
    Create visualization of rainfall patterns using filtered data
    Args:
        data: Iterable of weather data dicts
        output_path: Path to save the plot
    """
    logger.info("Creating rainfall patterns plot")

    # filter for rainy days only
    rainy_days = list(filter(
        lambda row: row.get('Rainfall') is not None
                    and isinstance(row['Rainfall'], (int, float))
                    and row['Rainfall'] > 0,
        data
    ))

    # extract rainfall amounts
    rainfall_amounts = list(map(lambda row: row['Rainfall'], rainy_days))

    if not rainfall_amounts:
        logger.warning("No rainfall data to plot")
        return

    plt.figure(figsize=(10, 6))
    plt.hist(rainfall_amounts, bins=50, edgecolor='black', alpha=0.7, color='blue')
    plt.xlabel('Rainfall Amount (mm)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Rainfall on Rainy Days')
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Rainfall patterns plot saved to {output_path}")


def plot_temperature_vs_humidity(data: Iterable[dict], output_path: str = 'temp_vs_humidity.png'):
    """
    Create scatter plot of temp vs humidity using filtered data
    Args:
        data: Iterable of weather data dicts
        output_path: Path to save the plot
    """
    logger.info("Creating temperature vs humidity scatter plot")

    # filter for valid data points
    valid_data = list(filter(
        lambda row: (row.get('MaxTemp') is not None and isinstance(row['MaxTemp'], (int, float)) and
                     row.get('Humidity3pm') is not None and isinstance(row['Humidity3pm'], (int, float))),
        data
    ))

    # extract values using map
    temps = list(map(lambda row: row['MaxTemp'], valid_data))
    humidity = list(map(lambda row: row['Humidity3pm'], valid_data))

    if not temps or not humidity:
        logger.warning("Insufficient data for temperature vs humidity plot")
        return

    plt.figure(figsize=(10, 6))
    plt.scatter(temps, humidity, alpha=0.3, s=10)
    plt.xlabel('Maximum Temperature (°C)')
    plt.ylabel('Humidity at 3pm (%)')
    plt.title('Temperature vs Humidity Relationship')
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Temperature vs humidity plot saved to {output_path}")


def plot_wind_speed_distribution(data: Iterable[dict], output_path: str = 'wind_speed_distribution.png'):
    """
    Create histogram of wind gust speeds using filtered data
    Args:
        data: Iterable of weather data dicts
        output_path: Path to save the plot
    """
    logger.info("Creating wind speed distribution plot")

    # use filter and map to extract valid wind speeds
    wind_speeds = list(filter(
        lambda x: x is not None,
        map(lambda row: row.get('WindGustSpeed') if isinstance(row.get('WindGustSpeed'), (int, float)) else None, data)
    ))

    if not wind_speeds:
        logger.warning("No valid wind speed data to plot")
        return

    plt.figure(figsize=(10, 6))
    plt.hist(wind_speeds, bins=50, edgecolor='black', alpha=0.7, color='green')
    plt.xlabel('Wind Gust Speed (km/h)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Wind Gust Speeds')
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Wind speed distribution plot saved to {output_path}")


def plot_pressure_vs_rain(data: Iterable[dict], output_path: str = 'pressure_vs_rain.png'):
    """
    Create box plot comparing pressure on rainy vs non rainy days
    Args:
        data: Iterable of weather data dicts
        output_path: Path to save the plot
    """
    logger.info("Creating pressure vs rain plot")

    data_list = list(data)

    # filter rainy and non rainy days
    rainy_days = list(filter(lambda row: row.get('RainToday') == 'Yes', data_list))
    non_rainy_days = list(filter(lambda row: row.get('RainToday') == 'No', data_list))

    # extract pressure values
    rainy_pressure = list(filter(
        lambda x: x is not None,
        map(lambda row: row.get('Pressure9am') if isinstance(row.get('Pressure9am'), (int, float)) else None, rainy_days)
    ))

    non_rainy_pressure = list(filter(
        lambda x: x is not None,
        map(lambda row: row.get('Pressure9am') if isinstance(row.get('Pressure9am'), (int, float)) else None, non_rainy_days)
    ))

    if not rainy_pressure or not non_rainy_pressure:
        logger.warning("Insufficient pressure data for comparison")
        return

    plt.figure(figsize=(10, 6))
    plt.boxplot([non_rainy_pressure, rainy_pressure], labels=['No Rain', 'Rain'])
    plt.ylabel('Pressure at 9am (hPa)')
    plt.title('Atmospheric Pressure: Rainy vs Non-Rainy Days')
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Pressure vs rain plot saved to {output_path}")


def plot_temperature_range_trends(data: Iterable[dict], output_path: str = 'temperature_range_trends.png'):
    """
    Create histogram of daily temp ranges
    Args:
        data: Iterable of weather data dicts
        output_path: Path to save the plot
    """
    logger.info("Creating temperature range trends plot")

    # calculate temp ranges using map and filter
    temp_ranges = extract_temperature_range(data)

    if not temp_ranges:
        logger.warning("No valid temperature range data to plot")
        return

    plt.figure(figsize=(10, 6))
    plt.hist(temp_ranges, bins=50, edgecolor='black', alpha=0.7, color='orange')
    plt.xlabel('Daily Temperature Range (°C)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Daily Temperature Ranges (MaxTemp - MinTemp)')
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Temperature range trends plot saved to {output_path}")
