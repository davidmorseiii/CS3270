from typing import Optional
from .data_loader import load_weather_data, csv_row_generator
from .data_cleaning import extract_valid_numeric_values, valid_numeric_values_generator
from .analytics import calculate_mean, calculate_median, calculate_range, calculate_statistics_streaming
from .logger_config import setup_logger

logger = setup_logger(__name__)


class WeatherDataset:
    """
    Class to represent the weather data and do analysis
    - Encapsulate data loading and statistical calculations
    - Provide eager and lazy loading options for memory efficiency
    """

    def __init__(self, file_path: str, lazy_load: bool = False):
        """
        Initialize the WeatherDataset
        Args:
            file_path: Path to the CSV file
            lazy_load: If True, data is loaded on demand. If False, loaded immediately
        Raises:
            FileNotFoundError: File doesn't exist
            ValueError: File is empty or messed up
        """
        self._file_path = file_path
        self._lazy_load = lazy_load
        self._data = None

        try:
            if not lazy_load:
                logger.info(f"Eagerly loading dataset from: {file_path}")
                self._data = load_weather_data(file_path)
                logger.info(f"Dataset loaded with {len(self._data)} rows")
            else:
                logger.info(f"Dataset iniitialized for lazy loading: {file_path}")

        except Exception as e:
            logger.error(f"Failed to initialize WeatherDataset: {e}")
            raise

    def _ensure_data_loaded(self):
        """Ensure data is loaded if lazy loading"""
        if self._lazy_load and self._data is None:
            logger.info(f"Lazy loading data from: {self._file_path}")
            self._data = load_weather_data(self._file_path)
            logger.info(f"Lazy loaded {len(self._data)} rows")

    def get_row_count(self) -> int:
        """
        Return the number of rows in the dataset
        Returns:
            Number of rows
        """
        try:
            self._ensure_data_loaded()
            count = len(self._data)
            logger.debug(f"Row count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error getting row count: {e}")
            raise

    def get_column_statistics(self, column_name: str) -> Optional[dict]:
        """
        Calculate stats for a specific column
        Args:
            column_name: Name of the column to analyze
        Returns:
            Dict with mean, median, range, or None if no valid data
        Raises:
            ValueError: Column doesn't exist
        """
        try:
            logger.info(f"Calculating statistics for column: {column_name}")
            self._ensure_data_loaded()

            # cleaning function
            valid_values = extract_valid_numeric_values(self._data, column_name)

            if not valid_values:
                logger.warning(f"No valid values found for column: {column_name}")
                return None

            # calculate all stats and return as a package
            result = {
                'mean': calculate_mean(valid_values),
                'median': calculate_median(valid_values),
                'range': calculate_range(valid_values)
            }

            logger.info(f"Statistics calculated for {column_name}: mean={result['mean']:.2f}, median={result['median']:.2f}, range={result['range']:.2f}")
            return result

        except Exception as e:
            logger.error(f"Error calculating statistics for column {column_name}: {e}")
            raise

    def get_column_statistics_streaming(self, column_name: str) -> Optional[dict]:
        """
        Calculate stats for a specific column using streaming for more memory efficiency
        Args:
            column_name: Name of the column to analyze
        Returns:
            Dict with mean, min, max, range, count, or None if no valid data
        Raises:
            ValueError: Column doesn't exist
        """
        try:
            logger.info(f"Calculating streaming statistics for column: {column_name}")

            # use generator to process data like streaming
            if self._lazy_load or self._data is None:
                # use CSV generator directly for true streaming
                data_generator = csv_row_generator(self._file_path)
            else:
                # use loaded data
                data_generator = iter(self._data)

            # get valid values as generator
            valid_values_gen = valid_numeric_values_generator(data_generator, column_name)

            # calculate statistics in streaming mode
            result = calculate_statistics_streaming(valid_values_gen)

            # add median (have to second pass to store value)
            if not self._lazy_load and self._data:
                valid_values = extract_valid_numeric_values(self._data, column_name)
                result['median'] = calculate_median(valid_values)
            else:
                logger.info("Median calculation skipped in pure streaming mode")
                result['median'] = None

            logger.info(f"Streaming statistics calculated for {column_name}")
            return result

        except Exception as e:
            logger.error(f"Error calculating streaming statistics for column {column_name}: {e}")
            raise

    def get_data(self) -> list[dict]:
        """
        Return the loaded data
        Returns:
            List of dicts containing weather data
        """
        try:
            self._ensure_data_loaded()
            logger.debug("Returning dataset")
            return self._data
        except Exception as e:
            logger.error(f"Error getting data: {e}")
            raise

    def iter_rows(self):
        """
        Return an iterator over the rows for memory efficient processing
        Yields:
            Dict for each row
        """
        try:
            if self._lazy_load or self._data is None:
                logger.debug("Using generator for row iteration")
                yield from csv_row_generator(self._file_path)
            else:
                logger.debug("Using loaded data for row iteration")
                yield from iter(self._data)
        except Exception as e:
            logger.error(f"Error iterating rows: {e}")
            raise