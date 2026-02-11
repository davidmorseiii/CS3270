"""
Unit tests with pytest and doctest.
Run pytest:
- pytest test_weather_analysis.py -v

Run pytest with doctests (4 doctests: basic calculate_mean, calculate_median (even and odd), and calculate_range):
- pytest test_weather_analysis.py --doctest-modules -v
"""

import pytest
import tempfile
import os
from weather_analysis import (
    calculate_mean,
    calculate_median,
    calculate_range,
    calculate_statistics_streaming,
    extract_valid_numeric_values,
    valid_numeric_values_generator,
    filter_rows_by_condition,
    load_weather_data,
    csv_row_generator,
    WeatherDataset
)

# -- Analytics --

class TestCalculateMean:
    """calculate_mean tests"""

    def test_mean_basic(self):
        """
        Basic mean calculation
        >>> calculate_mean([1, 2, 3, 4, 5])
        3.0
        """
        assert calculate_mean([1, 2, 3, 4, 5]) == 3.0

    def test_mean_negative_values(self):
        """Mean with negative values"""
        assert calculate_mean([-1, -2, -3, -4]) == -2.5

    def test_mean_mixed_values(self):
        """Mean with mixed positive and negative values"""
        assert calculate_mean([-10, 10, -5, 5]) == 0.0

    def test_mean_empty_list(self):
        """Mean raises ValueError for empty list"""
        with pytest.raises(ValueError, match="empty"):
            calculate_mean([])

    def test_mean_with_iterator(self):
        """Mean works with iterators"""
        assert calculate_mean(iter([2, 4, 6, 8])) == 5.0


class TestCalculateMedian:
    """calculate_median tests"""

    def test_median_odd_length(self):
        """
        Median with odd num of elements
        >>> calculate_median([1, 3, 5, 7, 9])
        5
        """
        assert calculate_median([1, 3, 5, 7, 9]) == 5

    def test_median_even_length(self):
        """
        Median with even num of elements
        >>> calculate_median([1, 2, 3, 4])
        2.5
        """
        assert calculate_median([1, 2, 3, 4]) == 2.5

    def test_median_unsorted(self):
        """Median with unsorted values"""
        assert calculate_median([5, 1, 3, 9, 2]) == 3

    def test_median_empty_list(self):
        """Median raises ValueError for empty list"""
        with pytest.raises(ValueError, match="empty"):
            calculate_median([])

    def test_median_with_iterator(self):
        """Median works with iterators"""
        assert calculate_median(iter([10, 20, 30])) == 20


class TestCalculateRange:
    """calculate_range tests"""

    def test_range_basic(self):
        """
        Basic range calculation
        >>> calculate_range([1, 5, 10])
        9
        """
        assert calculate_range([1, 5, 10]) == 9

    def test_range_negative_values(self):
        """Range with negative values"""
        assert calculate_range([-10, -5, -1]) == 9

    def test_range_mixed_values(self):
        """Range with mixed positive and negative"""
        assert calculate_range([-5, 0, 5, 10]) == 15

    def test_range_empty_list(self):
        """Range raises ValueError for empty list"""
        with pytest.raises(ValueError, match="empty"):
            calculate_range([])


class TestCalculateStatisticsStreaming:
    """calculate_statistics_streaming tests"""

    def test_streaming_basic(self):
        """Basic streaming statistics calculation"""
        values = iter([1, 2, 3, 4, 5])
        result = calculate_statistics_streaming(values)

        assert result['mean'] == 3.0
        assert result['min'] == 1
        assert result['max'] == 5
        assert result['range'] == 4
        assert result['count'] == 5

    def test_streaming_empty_iterator(self):
        """Streaming raises ValueError for empty iterator"""
        with pytest.raises(ValueError, match="empty"):
            calculate_statistics_streaming(iter([]))


# -- Data Cleaning ---

class TestValidNumericValuesGenerator:
    """valid_numeric_values_generator tests"""

    def test_generator_basic(self):
        """Basic generator functionality"""
        data = [
            {'temp': 25.5, 'humidity': 60},
            {'temp': 30.0, 'humidity': 55},
            {'temp': 28.3, 'humidity': 58}
        ]
        result = list(valid_numeric_values_generator(data, 'temp'))
        assert result == [25.5, 30.0, 28.3]

    def test_generator_filters_none(self):
        """Generator filters None values"""
        data = [
            {'temp': 25.5},
            {'temp': None},
            {'temp': 30.0}
        ]
        result = list(valid_numeric_values_generator(data, 'temp'))
        assert result == [25.5, 30.0]

    def test_generator_filters_nan(self):
        """Generator filters NaN values"""
        data = [
            {'temp': 25.5},
            {'temp': float('nan')},
            {'temp': 30.0}
        ]
        result = list(valid_numeric_values_generator(data, 'temp'))
        assert result == [25.5, 30.0]

    def test_generator_empty_data(self):
        """Generator raises ValueError for empty data"""
        with pytest.raises(ValueError, match="empty dataset"):
            list(valid_numeric_values_generator([], 'temp'))

    def test_generator_missing_column(self):
        """Generator raises ValueError for missing column"""
        data = [{'humidity': 60}]
        with pytest.raises(ValueError, match="not found"):
            list(valid_numeric_values_generator(data, 'temp'))


class TestExtractValidNumericValues:
    """extract_valid_numeric_values tests"""

    def test_extract_basic(self):
        """Basic extraction"""
        data = [
            {'MaxTemp': 25.5, 'MinTemp': 15.0},
            {'MaxTemp': 30.0, 'MinTemp': 18.0}
        ]
        result = extract_valid_numeric_values(data, 'MaxTemp')
        assert result == [25.5, 30.0]

    def test_extract_with_invalid_values(self):
        """Extraction filters invalid values"""
        data = [
            {'temp': 25.5},
            {'temp': None},
            {'temp': float('nan')},
            {'temp': 30.0}
        ]
        result = extract_valid_numeric_values(data, 'temp')
        assert result == [25.5, 30.0]


class TestFilterRowsByCondition:
    """filter_rows_by_condition tests"""

    def test_filter_basic(self):
        """Basic filtering"""
        data = [
            {'temp': 20, 'city': 'A'},
            {'temp': 30, 'city': 'B'},
            {'temp': 25, 'city': 'C'}
        ]
        result = list(filter_rows_by_condition(data, lambda row: row['temp'] > 22))
        assert len(result) == 2
        assert result[0]['city'] == 'B'
        assert result[1]['city'] == 'C'

    def test_filter_none_match(self):
        """Filtering with no matches"""
        data = [{'temp': 20}, {'temp': 21}]
        result = list(filter_rows_by_condition(data, lambda row: row['temp'] > 100))
        assert len(result) == 0

    def test_filter_all_match(self):
        """Filtering where all match"""
        data = [{'temp': 20}, {'temp': 30}]
        result = list(filter_rows_by_condition(data, lambda row: row['temp'] > 10))
        assert len(result) == 2

    def test_filter_non_callable(self):
        """Filter raises TypeError for uncallable condition"""
        data = [{'temp': 20}]
        with pytest.raises(TypeError, match="callable"):
            list(filter_rows_by_condition(data, "not a function"))


# -- Data Loader --

class TestCSVRowGenerator:
    """csv_row_generator tests"""

    def test_csv_generator_basic(self):
        """Basic CSV generation"""
        # create temp CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
            f.write('name,temp,humidity\n')
            f.write('Location1,25.5,60\n')
            f.write('Location2,30.0,55\n')
            temp_path = f.name

        try:
            rows = list(csv_row_generator(temp_path))
            assert len(rows) == 2
            assert rows[0]['name'] == 'Location1'
            assert rows[0]['temp'] == 25.5
            assert rows[1]['temp'] == 30.0
        finally:
            os.unlink(temp_path)

    def test_csv_generator_missing_file(self):
        """Generator raises FileNotFoundError for missing file"""
        with pytest.raises(FileNotFoundError):
            list(csv_row_generator('nonexistent_file.csv'))

    def test_csv_generator_empty_file(self):
        """Generator raises ValueError for empty CSV"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
            f.write('name,temp\n')  # only header, no data
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="empty"):
                list(csv_row_generator(temp_path))
        finally:
            os.unlink(temp_path)


class TestLoadWeatherData:
    """load_weather_data tests"""

    def test_load_basic(self):
        """Basic data loading"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
            f.write('Location,MaxTemp,MinTemp\n')
            f.write('Sydney,28.5,18.0\n')
            f.write('Melbourne,22.0,12.5\n')
            temp_path = f.name

        try:
            data = load_weather_data(temp_path)
            assert len(data) == 2
            assert data[0]['Location'] == 'Sydney'
            assert data[0]['MaxTemp'] == 28.5
        finally:
            os.unlink(temp_path)

    def test_load_missing_file(self):
        """Loading raises FileNotFoundError for missing file"""
        with pytest.raises(FileNotFoundError):
            load_weather_data('missing_file.csv')


# -- WeatherDataset Tests --

class TestWeatherDataset:
    """WeatherDataset class tests"""

    @pytest.fixture
    def sample_csv_file(self):
        """small csv file to test with"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
            f.write('Location,MaxTemp,MinTemp,Rainfall\n')
            f.write('Sydney,28.5,18.0,5.2\n')
            f.write('Melbourne,22.0,12.5,\n')
            f.write('Brisbane,30.0,20.5,2.1\n')
            temp_path = f.name

        yield temp_path

        # cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    def test_init_eager_loading(self, sample_csv_file):
        """Dataset initialization with eager loading"""
        dataset = WeatherDataset(sample_csv_file, lazy_load=False)
        assert dataset._data is not None
        assert len(dataset._data) == 3

    def test_init_lazy_loading(self, sample_csv_file):
        """Dataset initialization with lazy loading"""
        dataset = WeatherDataset(sample_csv_file, lazy_load=True)
        assert dataset._data is None

    def test_get_row_count(self, sample_csv_file):
        """Getting row count"""
        dataset = WeatherDataset(sample_csv_file)
        assert dataset.get_row_count() == 3

    def test_get_column_statistics(self, sample_csv_file):
        """Getting column statistics"""
        dataset = WeatherDataset(sample_csv_file)
        stats = dataset.get_column_statistics('MaxTemp')

        assert stats is not None
        assert 'mean' in stats
        assert 'median' in stats
        assert 'range' in stats
        assert stats['mean'] == pytest.approx(26.833, rel=0.01)

    def test_get_column_statistics_with_none(self, sample_csv_file):
        """Statistics handle None values correctly"""
        dataset = WeatherDataset(sample_csv_file)
        stats = dataset.get_column_statistics('Rainfall')

        # should only calculate from values 5.2 and 2.1
        assert stats is not None
        assert stats['mean'] == pytest.approx(3.65, rel=0.01)

    def test_get_data(self, sample_csv_file):
        """Getting the loaded data"""
        dataset = WeatherDataset(sample_csv_file)
        data = dataset.get_data()
        assert isinstance(data, list)
        assert len(data) == 3

    def test_iter_rows(self, sample_csv_file):
        """Iterating over rows"""
        dataset = WeatherDataset(sample_csv_file)
        rows = list(dataset.iter_rows())
        assert len(rows) == 3
        assert 'Location' in rows[0]

    def test_missing_file(self):
        """Dataset raises FileNotFoundError for missing file"""
        with pytest.raises(FileNotFoundError):
            WeatherDataset('nonexistent_file.csv')

    def test_lazy_loading_triggers_on_access(self, sample_csv_file):
        """Lazy loading loads data on first access"""
        dataset = WeatherDataset(sample_csv_file, lazy_load=True)
        assert dataset._data is None

        # access should trigger loading
        count = dataset.get_row_count()
        assert dataset._data is not None
        assert count == 3


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
