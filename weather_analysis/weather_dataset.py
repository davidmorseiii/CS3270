from .load_csv_to_df import load_weather_data
from .data_cleaning import extract_valid_temperatures
from .analytics import calculate_mean, calculate_median, calculate_range

class WeatherDataset:
    """
    Class to represent the weather data and perform analysis.
    Encapsulates the data loading and statistical calculations.
    """
    def __init__(self, file_path):
        # load data immediately when the object is created
        # _data to indicate it's for internal use
        self._data = load_weather_data(file_path)

    def get_row_count(self):
        return len(self._data)

    def get_column_statistics(self, column_name):
        """
        Calculates stats for a specific column.
        Returns:
            Dictionary with mean, median, range, or None if no valid data.
        """
        # reuse existing cleaning function
        valid_values = extract_valid_temperatures(self._data, column_name)

        if not valid_values:
            return None

        # calculate all stats and return them as a package
        return {
            'mean': calculate_mean(valid_values),
            'median': calculate_median(valid_values),
            'range': calculate_range(valid_values)
        }