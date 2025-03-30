"""Tests for the Flask application and HelloWorldService.

This module contains test cases for both the Flask routes and the HelloWorldService class.
"""

import pytest
from datetime import datetime, timezone
from main import app
from helloworld import HelloWorldService
from request_handler import parse_hello_json


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def app_context():
    """Create an application context for testing."""
    with app.app_context():
        yield


class TestHelloWorldService:
    """Test cases for HelloWorldService class."""

    @pytest.fixture
    def service(self, app_context):
        """Create a fresh HelloWorldService instance for each test."""
        return HelloWorldService()

    def test_initialization(self, service):
        """Test service initialization with default values."""
        assert service.name == 'world'
        assert isinstance(service.date, datetime)

    def test_set_values_with_datetime(self, service):
        """Test setting values with datetime object."""
        test_name = "Test User"
        test_date = datetime(2024, 1, 1, 12, 0)
        
        service.set_values(test_name, test_date)
        assert service.name == test_name
        assert service.date == test_date

    def test_set_values_with_string_timestamp(self, service):
        """Test setting values with ISO format string timestamp."""
        test_name = "Test User"
        test_date_str = "2024-01-01T12:00:00"
        
        service.set_values(test_name, test_date_str)
        assert service.name == test_name
        assert service.date == datetime.fromisoformat(test_date_str)

    def test_set_values_with_utc_timestamp(self, service):
        """Test setting values with UTC timestamp."""
        test_name = "Test User"
        test_date = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
        
        service.set_values(test_name, test_date)
        assert service.name == test_name
        assert service.date == test_date

    def test_set_values_with_microseconds(self, service):
        """Test setting values with timestamp including microseconds."""
        test_name = "Test User"
        test_date = datetime(2024, 1, 1, 12, 0, 0, 123456)
        
        service.set_values(test_name, test_date)
        assert service.name == test_name
        assert service.date == test_date

    def test_set_values_with_isoformat_microseconds(self, service):
        """Test setting values with ISO format string including microseconds."""
        test_name = "Test User"
        test_date_str = "2024-01-01T12:00:00.123456"
        
        service.set_values(test_name, test_date_str)
        assert service.name == test_name
        assert service.date == datetime.fromisoformat(test_date_str)

    def test_set_values_invalid_timestamp(self, service):
        """Test setting values with invalid timestamp format."""
        with pytest.raises(ValueError, match="Invalid timestamp format"):
            service.set_values("Test User", "invalid-date")

    def test_set_values_empty_timestamp(self, service):
        """Test setting values with empty timestamp string."""
        with pytest.raises(ValueError, match="Invalid timestamp format"):
            service.set_values("Test User", "")

    def test_set_values_none_timestamp(self, service):
        """Test setting values with None timestamp."""
        with pytest.raises(ValueError, match="Invalid timestamp format"):
            service.set_values("Test User", None)

    def test_set_values_empty_name(self, service):
        """Test setting values with empty name."""
        test_date = datetime(2024, 1, 1, 12, 0)
        service.set_values("", test_date)
        assert service.name == ""
        assert service.date == test_date

    def test_set_values_whitespace_name(self, service):
        """Test setting values with whitespace-only name."""
        test_date = datetime(2024, 1, 1, 12, 0)
        service.set_values("   ", test_date)
        assert service.name == "   "
        assert service.date == test_date

    def test_say_hello_default(self, service):
        """Test the say_hello method with default values."""
        response = service.say_hello()
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'json_data' in data
        assert len(data['json_data']) == 1
        assert 'message' in data['json_data'][0]
        assert 'time' in data['json_data'][0]
        assert data['json_data'][0]['message'] == 'Hello world'

    def test_say_hello_custom_name(self, service):
        """Test the say_hello method with custom name."""
        service.set_values("Custom Name", datetime(2024, 1, 1, 12, 0))
        response = service.say_hello()
        
        data = response.get_json()
        assert data['json_data'][0]['message'] == 'Hello Custom Name'

    def test_say_hello_response_format(self, service):
        """Test the say_hello method response format in detail."""
        test_date = datetime(2024, 1, 1, 12, 0)
        service.set_values("Test User", test_date)
        response = service.say_hello()
        
        data = response.get_json()
        assert response.mimetype == 'application/json'
        assert data['status'] == 200
        assert isinstance(data['json_data'], list)
        assert len(data['json_data']) == 1
        assert isinstance(data['json_data'][0], dict)
        assert 'message' in data['json_data'][0]
        assert 'time' in data['json_data'][0]
        assert isinstance(data['json_data'][0]['time'], str)
        assert data['json_data'][0]['time'] == test_date.isoformat()


class TestFlaskRoutes:
    """Test cases for Flask routes."""

    def test_index_route(self, client):
        """Test the index route."""
        response = client.get('/')
        assert response.status_code == 200
        assert response.data == b'devcontainers: Index Page'

    def test_hello_get_route(self, client):
        """Test the hello route with GET method."""
        response = client.get('/hello')
        assert response.status_code == 200
        data = response.get_json()
        assert 'json_data' in data
        assert len(data['json_data']) == 1
        assert 'message' in data['json_data'][0]
        assert 'time' in data['json_data'][0]

    def test_hello_post_route_valid_data(self, client):
        """Test the hello route with POST method and valid data."""
        test_data = {
            "name": "Test User",
            "timestamp": "2024-01-01T12:00:00"
        }
        response = client.post('/hello', json=test_data)
        assert response.status_code == 200
        data = response.get_json()
        assert 'json_data' in data
        assert len(data['json_data']) == 1
        assert data['json_data'][0]['message'] == 'Hello Test User'

    def test_hello_post_route_missing_data(self, client):
        """Test the hello route with POST method and missing data."""
        response = client.post('/hello', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Request must include JSON data' == data['error']

    def test_hello_post_route_invalid_timestamp(self, client):
        """Test the hello route with POST method and invalid timestamp."""
        test_data = {
            "name": "Test User",
            "timestamp": "invalid-date"
        }
        response = client.post('/hello', json=test_data)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid timestamp format' in data['error']

    def test_hello_route_invalid_method(self, client):
        """Test the hello route with invalid HTTP method."""
        response = client.put('/hello')
        assert response.status_code == 405
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Method not allowed'


class TestRequestHandler:
    """Test cases for request handling functionality."""

    def test_parse_hello_json_valid_data(self):
        """Test parsing valid JSON data."""
        json_data = {
            "name": "Test User",
            "timestamp": "2024-01-01T12:00:00"
        }
        name, timestamp = parse_hello_json(json_data)
        assert name == "Test User"
        assert timestamp == "2024-01-01T12:00:00"

    def test_parse_hello_json_with_datetime(self):
        """Test parsing JSON with datetime object."""
        test_date = datetime(2024, 1, 1, 12, 0)
        json_data = {
            "name": "Test User",
            "timestamp": test_date
        }
        name, timestamp = parse_hello_json(json_data)
        assert name == "Test User"
        assert timestamp == test_date

    def test_parse_hello_json_missing_data(self):
        """Test parsing JSON with missing required fields."""
        json_data = {"name": "Test User"}
        with pytest.raises(ValueError, match="Missing required field"):
            parse_hello_json(json_data)

    def test_parse_hello_json_empty_data(self):
        """Test parsing empty JSON data."""
        with pytest.raises(ValueError, match="Request must include JSON data"):
            parse_hello_json({})

    def test_parse_hello_json_none_data(self):
        """Test parsing None JSON data."""
        with pytest.raises(ValueError, match="Request must include JSON data"):
            parse_hello_json(None)

    def test_parse_hello_json_invalid_name_type(self):
        """Test parsing JSON with invalid name type."""
        json_data = {
            "name": 123,  # Should be string
            "timestamp": "2024-01-01T12:00:00"
        }
        with pytest.raises(ValueError, match="Name must be a string"):
            parse_hello_json(json_data)

    def test_parse_hello_json_empty_name(self):
        """Test parsing JSON with empty name."""
        json_data = {
            "name": "",
            "timestamp": "2024-01-01T12:00:00"
        }
        name, timestamp = parse_hello_json(json_data)
        assert name == ""
        assert timestamp == "2024-01-01T12:00:00"

    def test_parse_hello_json_whitespace_name(self):
        """Test parsing JSON with whitespace-only name."""
        json_data = {
            "name": "   ",
            "timestamp": "2024-01-01T12:00:00"
        }
        name, timestamp = parse_hello_json(json_data)
        assert name == "   "
        assert timestamp == "2024-01-01T12:00:00"

    def test_parse_hello_json_with_utc_timestamp(self):
        """Test parsing JSON with UTC timestamp."""
        test_date = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
        json_data = {
            "name": "Test User",
            "timestamp": test_date
        }
        name, timestamp = parse_hello_json(json_data)
        assert name == "Test User"
        assert timestamp == test_date

    def test_parse_hello_json_with_microseconds(self):
        """Test parsing JSON with timestamp including microseconds."""
        test_date = datetime(2024, 1, 1, 12, 0, 0, 123456)
        json_data = {
            "name": "Test User",
            "timestamp": test_date
        }
        name, timestamp = parse_hello_json(json_data)
        assert name == "Test User"
        assert timestamp == test_date 