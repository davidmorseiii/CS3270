from typing import Iterable, Iterator
from itertools import islice
from .logger_config import setup_logger

logger = setup_logger(__name__)

def calculate_mean(values: Iterable[float]) -> float:
    """
    Calculate the average of a collection of numbers (lists or iterators)
    Args:
        values: Iterable of numeric values
    Returns:
        Mean value
    Raises:
        ValueError: Values is empty
        TypeError: Values contain non numeric types
    """
    try:
        # convert to list if its an iterator
        if not isinstance(values, list):
            values = list(values)

        if not values:
            logger.error("Cannot calculate mean of empty collection")
            raise ValueError("Can't calculate mean of empty list")

        logger.debug(f"Calculating mean of {len(values)} values")
        result = sum(values) / len(values)
        logger.debug(f"Mean calcalulated: {result}")
        return result

    except TypeError as e:
        logger.error(f"Type error in calculate_mean: {e}")
        raise TypeError(f"All values must be numeric: {e}")
    except Exception as e:
        logger.error(f"Error calculating mean: {e}")
        raise


def calculate_median(values: Iterable[float]) -> float:
    """
    Calculate the median of collection of numbers (lists or iterators)
    Args:
        values: Iterable of numeric values
    Returns:
        Median value
    Raises:
        ValueError: values is empty
    """
    try:
        # convert to list if it's an iterator
        if not isinstance(values, list):
            values = list(values)

        if not values:
            logger.error("Cannot calculate median of empty collection")
            raise ValueError("Can't calculate median of empty list")

        logger.debug(f"Calculating median of {len(values)} values")
        sorted_values = sorted(values)
        n = len(sorted_values)

        # if odd num of elements, return middle value
        if n % 2 == 1:
            result = sorted_values[n // 2]
        # if even num of elements, return avg of two middle values
        else:
            mid1 = sorted_values[n // 2 - 1]
            mid2 = sorted_values[n // 2]
            result = (mid1 + mid2) / 2

        logger.debug(f"Median calculated: {result}")
        return result

    except Exception as e:
        logger.error(f"Error calculating median: {e}")
        raise


def calculate_range(values: Iterable[float]) -> float:
    """
    Calculate the range of a collection of numbers (lists or iterators)
    Args:
        values: Iterable of numeric values
    Returns:
        Range value
    Raises:
        ValueError: values is empty
    """
    try:
        # convert to list if it's an iterator
        if not isinstance(values, list):
            values = list(values)

        if not values:
            logger.error("Cannot calculate range of empty collection")
            raise ValueError("Can't calculate range of empty list")

        logger.debug(f"Calculating range of {len(values)} values")
        result = max(values) - min(values)
        logger.debug(f"Range calculated: {result}")
        return result

    except Exception as e:
        logger.error(f"Error calculating range: {e}")
        raise


def calculate_statistics_streaming(values: Iterator[float]) -> dict:
    """
    Calculate mean, min, max, and count in single pass through data. Memory efficient for large dataset using generator pattern
    Args:
        values: Iterator of numeric values
    Returns:
        Dict with 'mean', 'min', 'max', 'count', 'range' keys
    Raises:
        ValueError: Values is empty
    """
    try:
        logger.debug("Calculating statistics in streaming mode")

        count = 0
        total = 0
        min_val = float('inf')
        max_val = float('-inf')

        for value in values:
            count += 1
            total += value
            min_val = min(min_val, value)
            max_val = max(max_val, value)

        if count == 0:
            logger.error("Cannot calculate statistics of empty collection")
            raise ValueError("Cant calculate statistics of empty iterator")

        mean = total / count
        range_val = max_val - min_val

        result = {
            'mean': mean,
            'min': min_val,
            'max': max_val,
            'range': range_val,
            'count': count
        }

        logger.info(f"Streaming statistics calculated for {count} values: mean={mean:.2f}, range={range_val:.2f}")
        return result

    except Exception as e:
        logger.error(f"Error in calculate_statistics_streaming: {e}")
        raise