"""Unit tests for the request handler module.

This module contains test cases for request parsing and validation functionality.
"""

import pytest
from datetime import datetime, timezone
from request_handler import parse_hello_json


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

    def test_parse_hello_json_missing_timestamp(self):
        """Test parsing JSON with missing timestamp field."""
        json_data = {"name": "Test User"}
        with pytest.raises(ValueError, match="Missing required field"):
            parse_hello_json(json_data)

    def test_parse_hello_json_missing_name(self):
        """Test parsing JSON with missing name field."""
        json_data = {"timestamp": "2024-01-01T12:00:00"}
        with pytest.raises(ValueError, match="Missing required field"):
            parse_hello_json(json_data)

    def test_parse_hello_json_invalid_timestamp_type(self):
        """Test parsing JSON with invalid timestamp type."""
        json_data = {
            "name": "Test User",
            "timestamp": 123  # Should be string or datetime
        }
        name, timestamp = parse_hello_json(json_data)
        assert name == "Test User"
        assert timestamp == 123  # Currently accepts any type for timestamp 