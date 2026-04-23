"""
Unit tests with pytest and doctest.
Run pytest:
- pytest test_weather_analysis.py -v

Run pytest with doctests (4 doctests: basic calculate_mean, calculate_median (even and odd), and calculate_range):
- pytest test_weather_analysis.py --doctest-modules -v
"""

# To do: implement tests for Moudle 6 analytics
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
    WeatherDataset,
    filter_by_rainfall_threshold,
    filter_high_temperature_days,
    filter_windy_days,
    filter_by_location,
    extract_temperature_range,
    extract_humidity_change,
    extract_pressure_change,
    calculate_total_rainfall,
    find_max_temperature,
    find_min_temperature,
    count_rainy_days,
    analyze_rain_patterns
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


# -- Visualization Module Tests --

class TestFilterFunctions:
    """Test filter functions"""

    @pytest.fixture
    def sample_weather_data(self):
        """Sample data for testing"""
        return [
            {'Location': 'Sydney', 'MaxTemp': 30.0, 'MinTemp': 20.0, 'Rainfall': 5.5, 'WindGustSpeed': 45.0, 'RainToday': 'Yes'},
            {'Location': 'Melbourne', 'MaxTemp': 36.0, 'MinTemp': 22.0, 'Rainfall': 12.0, 'WindGustSpeed': 65.0, 'RainToday': 'No'},
            {'Location': 'Sydney', 'MaxTemp': 25.0, 'MinTemp': 18.0, 'Rainfall': 0.0, 'WindGustSpeed': 30.0, 'RainToday': 'No'},
            {'Location': 'Brisbane', 'MaxTemp': 38.0, 'MinTemp': 25.0, 'Rainfall': 15.5, 'WindGustSpeed': 70.0, 'RainToday': 'Yes'},
        ]

    def test_filter_rainfall_threshold(self, sample_weather_data):
        """Test filtering by rainfall threshold"""
        result = filter_by_rainfall_threshold(sample_weather_data, 10.0)
        assert len(result) == 2
        assert all(row['Rainfall'] >= 10.0 for row in result)

    def test_filter_high_temperature(self, sample_weather_data):
        """Test filtering by high temp"""
        result = filter_high_temperature_days(sample_weather_data, 35.0)
        assert len(result) == 2
        assert all(row['MaxTemp'] >= 35.0 for row in result)

    def test_filter_windy_days(self, sample_weather_data):
        """Test filtering by wind speed"""
        result = filter_windy_days(sample_weather_data, 60.0)
        assert len(result) == 2
        assert all(row['WindGustSpeed'] >= 60.0 for row in result)

    def test_filter_by_location(self, sample_weather_data):
        """Test filtering by location"""
        result = filter_by_location(sample_weather_data, 'Sydney')
        assert len(result) == 2
        assert all(row['Location'] == 'Sydney' for row in result)


class TestTransformFunctions:
    """Test transformation functions"""

    @pytest.fixture
    def sample_weather_data(self):
        """Sample weather data for testing"""
        return [
            {'MaxTemp': 30.0, 'MinTemp': 20.0, 'Humidity9am': 70, 'Humidity3pm': 60, 'Pressure9am': 1015.0, 'Pressure3pm': 1013.0},
            {'MaxTemp': 35.0, 'MinTemp': 22.0, 'Humidity9am': 65, 'Humidity3pm': 50, 'Pressure9am': 1018.0, 'Pressure3pm': 1016.0},
            {'MaxTemp': 25.0, 'MinTemp': 18.0, 'Humidity9am': 80, 'Humidity3pm': 70, 'Pressure9am': 1012.0, 'Pressure3pm': 1010.0},
        ]

    def test_extract_temperature_range(self, sample_weather_data):
        """Test temperature range extraction"""
        result = extract_temperature_range(sample_weather_data)
        assert len(result) == 3
        assert result[0] == 10.0
        assert result[1] == 13.0
        assert result[2] == 7.0

    def test_extract_humidity_change(self, sample_weather_data):
        """Test humidity change extraction"""
        result = extract_humidity_change(sample_weather_data)
        assert len(result) == 3
        assert result[0] == -10
        assert result[1] == -15
        assert result[2] == -10

    def test_extract_pressure_change(self, sample_weather_data):
        """Test pressure change extraction"""
        result = extract_pressure_change(sample_weather_data)
        assert len(result) == 3
        assert result[0] == -2.0
        assert result[1] == -2.0
        assert result[2] == -2.0


class TestAggregateFunctions:
    """Test aggregation functions"""

    @pytest.fixture
    def sample_weather_data(self):
        """Sample data for testing"""
        return [
            {'MaxTemp': 30.0, 'MinTemp': 15.0, 'Rainfall': 5.5},
            {'MaxTemp': 35.0, 'MinTemp': 10.0, 'Rainfall': 12.0},
            {'MaxTemp': 25.0, 'MinTemp': 20.0, 'Rainfall': 0.0},
            {'MaxTemp': 40.0, 'MinTemp': 8.0, 'Rainfall': 3.5},
        ]

    def test_calculate_total_rainfall(self, sample_weather_data):
        """Test total rainfall calculation using reduce"""
        result = calculate_total_rainfall(sample_weather_data)
        assert result == 21.0

    def test_find_max_temperature(self, sample_weather_data):
        """Test finding max temp using reduce"""
        result = find_max_temperature(sample_weather_data)
        assert result == 40.0

    def test_find_min_temperature(self, sample_weather_data):
        """Test finding min temp using reduce"""
        result = find_min_temperature(sample_weather_data)
        assert result == 8.0


# Auth, Upload, and Dashboard API tests

import io
import base64
from app import app as flask_app
from models import db, User


@pytest.fixture
def client():
    """Flask test client with in memory SQLite DB and a seeded test user"""
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SECRET_KEY'] = 'test-secret'

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        user = User(username='testuser')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()

    with flask_app.test_client() as c:
        yield c


@pytest.fixture
def auth_client(client):
    """Test client already logged in as testuser."""
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'},
                follow_redirects=False)
    return client


SAMPLE_CSV_CONTENT = (
    b"Location,MinTemp,MaxTemp,Rainfall,RainToday,WindGustSpeed\n"
    b"Sydney,15.0,28.5,0.0,No,45.0\n"
    b"Sydney,14.2,32.1,5.2,Yes,60.0\n"
    b"Melbourne,10.0,22.0,12.5,Yes,70.0\n"
    b"Melbourne,8.5,18.3,0.0,No,35.0\n"
    b"Adelaide,20.0,38.5,0.0,No,55.0\n"
)


class TestAuthLogic:
    def test_user_password_hashing(self):
        """set_password hashes the password; check_password validates it."""
        with flask_app.app_context():
            u = User(username='hashtest')
            u.set_password('hunter2')
            assert u.check_password('hunter2') is True
            assert u.check_password('wrong') is False
            assert u.password_hash != 'hunter2'

    def test_login_valid_credentials(self, client):
        """Correct credentials redirect to /upload."""
        resp = client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        assert resp.status_code == 302
        assert '/upload' in resp.headers['Location']

    def test_login_invalid_credentials(self, client):
        """Wrong password stays on login page with an error."""
        resp = client.post('/login', data={'username': 'testuser', 'password': 'wrongpass'})
        assert resp.status_code == 200
        assert b'Invalid username or password' in resp.data

    def test_protected_routes_redirect_unauthenticated(self, client):
        """All protected routes redirect to /login when not authenticated."""
        for path in ['/', '/analysis', '/locations', '/dashboard']:
            resp = client.get(path)
            assert resp.status_code == 302, f'{path} should redirect'
            assert '/login' in resp.headers['Location'], f'{path} should redirect to /login'

    def test_logout_clears_session(self, auth_client):
        """After logout, protected routes redirect to /login."""
        resp = auth_client.get('/logout')
        assert resp.status_code == 302
        assert '/login' in resp.headers['Location']
        resp2 = auth_client.get('/')
        assert resp2.status_code == 302
        assert '/login' in resp2.headers['Location']


class TestCSVUploadValidation:
    def _upload(self, client, content, filename='data.csv'):
        return client.post(
            '/upload',
            data={'csv_file': (io.BytesIO(content), filename)},
            content_type='multipart/form-data',
        )

    def test_upload_valid_csv(self, auth_client):
        """Valid CSV with all required columns redirects to /dashboard."""
        resp = self._upload(auth_client, SAMPLE_CSV_CONTENT)
        assert resp.status_code == 302
        assert '/dashboard' in resp.headers['Location']

    def test_upload_missing_column(self, auth_client):
        """CSV missing the Location column shows an error."""
        bad = b"MinTemp,MaxTemp,Rainfall,RainToday\n10.0,25.0,0.0,No\n"
        resp = self._upload(auth_client, bad)
        assert resp.status_code == 200
        assert b'Missing required columns' in resp.data or b'Location' in resp.data

    def test_upload_empty_csv(self, auth_client):
        """CSV with header only (no data rows) shows an error."""
        header_only = b"Location,MinTemp,MaxTemp,Rainfall,RainToday\n"
        resp = self._upload(auth_client, header_only)
        assert resp.status_code == 200
        assert b'no data rows' in resp.data.lower() or b'error' in resp.data.lower()

    def test_upload_non_csv_extension(self, auth_client):
        """Non-.csv file extension is rejected."""
        resp = self._upload(auth_client, SAMPLE_CSV_CONTENT, filename='data.txt')
        assert resp.status_code == 200
        assert b'Only .csv' in resp.data

    def test_upload_no_file(self, auth_client):
        """Submitting the upload form with no file shows an error."""
        resp = auth_client.post('/upload', data={}, content_type='multipart/form-data')
        assert resp.status_code == 200
        assert b'No file selected' in resp.data


class TestDashboardAPI:
    def _upload_sample(self, client):
        client.post(
            '/upload',
            data={'csv_file': (io.BytesIO(SAMPLE_CSV_CONTENT), 'data.csv')},
            content_type='multipart/form-data',
        )

    def test_api_cities_no_upload(self, auth_client):
        """GET /api/cities without an uploaded CSV returns 400."""
        resp = auth_client.get('/api/cities')
        assert resp.status_code == 400
        data = resp.get_json()
        assert 'error' in data

    def test_api_cities_returns_sorted_list(self, auth_client):
        """After upload, /api/cities returns a sorted list of location names."""
        self._upload_sample(auth_client)
        resp = auth_client.get('/api/cities')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'cities' in data
        assert data['cities'] == sorted(data['cities'])
        assert 'Sydney' in data['cities']
        assert 'Melbourne' in data['cities']

    def test_api_chart_invalid_category(self, auth_client):
        """Invalid category query param returns 400."""
        self._upload_sample(auth_client)
        resp = auth_client.get('/api/chart?category=invalid&city=Sydney')
        assert resp.status_code == 400

    def test_api_chart_missing_city(self, auth_client):
        """Missing city param returns 400."""
        self._upload_sample(auth_client)
        resp = auth_client.get('/api/chart?category=temperature')
        assert resp.status_code == 400
        data = resp.get_json()
        assert 'City is required' in data['error']

    def test_api_chart_unknown_city(self, auth_client):
        """City not present in the data returns 404."""
        self._upload_sample(auth_client)
        resp = auth_client.get('/api/chart?category=temperature&city=Atlantis')
        assert resp.status_code == 404

    def test_api_chart_temperature_returns_charts(self, auth_client):
        """Temperature category returns charts and a non-empty summary."""
        self._upload_sample(auth_client)
        resp = auth_client.get('/api/chart?category=temperature&city=Sydney')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'charts' in data and len(data['charts']) >= 1
        assert 'summary' in data and len(data['summary']) > 0
        # each chart must be valid base64
        for chart in data['charts']:
            base64.b64decode(chart)  # raises if invalid

    def test_api_chart_rainfall_category(self, auth_client):
        """Rainfall category returns charts and summary."""
        self._upload_sample(auth_client)
        resp = auth_client.get('/api/chart?category=rainfall&city=Sydney')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'charts' in data and len(data['charts']) >= 1
        assert 'summary' in data and len(data['summary']) > 0

    def test_api_chart_extreme_category(self, auth_client):
        """Extreme weather category returns charts and summary."""
        self._upload_sample(auth_client)
        resp = auth_client.get('/api/chart?category=extreme&city=Sydney')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'charts' in data and len(data['charts']) >= 1
        assert 'summary' in data and len(data['summary']) > 0


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
