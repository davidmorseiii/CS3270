import math
from typing import Iterator, Iterable
from .logger_config import setup_logger

logger = setup_logger(__name__)

def valid_numeric_values_generator(data: Iterable[dict], column_name: str) -> Iterator[float]:
    """
    Generator to yield valid numeric values from colunm in the dataset, filtering None, NaN, and non numeric values
    Args:
        data: Iterable of dicts containing weather data
        column_name: Name of the column to extract
    Yields:
        Valid num values as floats
    Raises:
        ValueError: Data is empty or column_name doesnt exist
    """
    try:
        # convert to iterator if it isn't already
        data_iter = iter(data)

        # check first row if column exists
        try:
            first_row = next(data_iter)
        except StopIteration:
            logger.error("Can't extract values from empty dataset")
            raise ValueError("Can't extract values from empty dataset")

        if column_name not in first_row:
            logger.error(f"Column '{column_name}' not found in dataset")
            raise ValueError(f"Column '{column_name}' not found in dataset")

        # process first row
        val = first_row.get(column_name)
        if val is not None and isinstance(val, (int, float)) and not math.isnan(val):
            yield float(val)

        # process remaining
        valid_count = 0
        invalid_count = 0

        for row_num, row in enumerate(data_iter, start=2):
            try:
                val = row.get(column_name)
                if val is not None and isinstance(val, (int, float)) and not math.isnan(val):
                    valid_count += 1
                    yield float(val)
                else:
                    invalid_count += 1
            except Exception as e:
                logger.debug(f"Error processing row {row_num}, column '{column_name}': {e}")
                invalid_count += 1
                continue

        logger.info(f"Extracted {valid_count} valid values from column '{column_name}', skipped {invalid_count} invalid values")

    except Exception as e:
        logger.error(f"Error in valid_numeric_values_generator for column '{column_name}': {e}")
        raise


def extract_valid_numeric_values(data: Iterable[dict], column_name: str) -> list[float]:
    """
    Extract valid num values from weather data, filtering None and NaN values. Uses generator for efficient memory usage
    Args:
        data: Iterable of dicts containing weather data
        column_name: Name of the column to extract
    Returns:
        List of valid numeric values
    Raises:
        ValueError: If data is empty or column_name doesn't exist in data
    """
    try:
        logger.debug(f"Extracting valid numeric values from column: {column_name}")
        values = list(valid_numeric_values_generator(data, column_name))
        logger.debug(f"Extracted {len(values)} valid values from column '{column_name}'")
        return values
    except Exception as e:
        logger.error(f"Failed to extract values from column '{column_name}': {e}")
        raise


def filter_rows_by_condition(data: Iterable[dict], condition_func: callable) -> Iterator[dict]:
    """
    Generator that filters rows based on a condition function
    Args:
        data: Iterable of dicts containing data
        condition_func: Takes a row dict and returns True/False
    Yields:
        Rows that satisfy the condition
    Raises:
        ValueError: Data is empty
        TypeError: Condition_func is not callable
    """
    if not callable(condition_func):
        logger.error("condition_func must be callable")
        raise TypeError("condition_func must be callable")

    try:
        data_iter = iter(data)
        row_count = 0
        filtered_count = 0

        for row in data_iter:
            row_count += 1
            try:
                if condition_func(row):
                    filtered_count += 1
                    yield row
            except Exception as e:
                logger.warning(f"Error evaluating condition for row {row_count}: {e}")
                continue

        logger.info(f"Filtered {filtered_count} rows out of {row_count} total rows")

    except Exception as e:
        logger.error(f"Error in filter_rows_by_condition: {e}")
        raise
