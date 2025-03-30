"""Service for handling hello world functionality.

This module provides a service class that manages greeting messages
and timestamps for the hello world application.
"""

from typing import Union, Dict, Any
from datetime import datetime
from flask import jsonify


class HelloWorldService:
    """Service class for managing hello world greetings.

    This class handles the creation and formatting of hello world messages
    with associated timestamps.
    """

    def __init__(self) -> None:
        """Initialize the service with default values."""
        self.name: str = 'world'
        self.date: datetime = datetime.now()

    def set_values(self, name: str, timestamp: Union[datetime, str]) -> None:
        """Set the name and timestamp for the greeting.

        Args:
            name: The name to use in the greeting
            timestamp: The timestamp to associate with the greeting

        Raises:
            ValueError: If the timestamp is invalid
        """
        self.name = name
        if timestamp is None:
            raise ValueError("Invalid timestamp format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
        if isinstance(timestamp, str):
            try:
                self.date = datetime.fromisoformat(timestamp)
            except ValueError:
                raise ValueError("Invalid timestamp format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
        else:
            self.date = timestamp

    def say_hello(self) -> Dict[str, Any]:
        """Generate a hello world message with timestamp.

        Returns:
            Dict[str, Any]: A dictionary containing the message and timestamp
        """
        val = [
            {'message': f'Hello {self.name}', 'time': self.date.isoformat()}
        ]
        return jsonify(json_data=val, status=200, mimetype='application/json')
