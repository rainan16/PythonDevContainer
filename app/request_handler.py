"""Request handling module for the hello world application.

This module provides functionality for parsing and validating incoming requests,
particularly focusing on JSON payload handling.
"""

from typing import Tuple, Dict, Any, Union
from datetime import datetime


def parse_hello_json(json_data: Dict[str, Any]) -> Tuple[str, Union[datetime, str]]:
    """Parse and validate hello world JSON request data.

    Args:
        json_data: Dictionary containing the request data

    Returns:
        Tuple[str, Union[datetime, str]]: A tuple containing the name and timestamp

    Raises:
        ValueError: If the JSON data is invalid or missing required fields
    """
    if not json_data:
        raise ValueError("Request must include JSON data")

    try:
        req_name: str = json_data['name']
        req_timestamp = json_data['timestamp']
    except KeyError as err:
        raise ValueError(f"Missing required field in JSON: {err}")

    if not isinstance(req_name, str):
        raise ValueError("Name must be a string")

    return req_name, req_timestamp
