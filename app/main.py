"""Flask application for handling hello world requests.

This module provides endpoints for basic hello world functionality,
supporting both GET and POST requests with JSON payloads.
"""

from typing import Tuple, Dict, Any, Union
from flask import Flask, request, jsonify
from werkzeug.exceptions import MethodNotAllowed
from helloworld import HelloWorldService
from request_handler import parse_hello_json

app = Flask(__name__)
hello_service = HelloWorldService()


@app.errorhandler(MethodNotAllowed)
def handle_405(e):
    """Handle 405 Method Not Allowed error."""
    return jsonify({'error': 'Method not allowed'}), 405


@app.route('/', methods=['GET'])
def index() -> str:
    """Index page.

    Returns:
        str: A welcome message for the index page.
    """
    return 'devcontainers: Index Page'


@app.route('/hello', methods=['GET', 'POST'])
def hello() -> Union[Tuple[str, int], Tuple[Dict[str, Any], int]]:
    """Hello world page (POST and GET).

    For POST requests, expects JSON with:
        - name (str): Name to include in the greeting
        - timestamp (str): ISO format timestamp (YYYY-MM-DDTHH:MM:SS) or datetime object

    Returns:
        Union[Tuple[str, int], Tuple[Dict[str, Any], int]]: A tuple containing
            the response message and HTTP status code.
    """
    if request.method == 'GET':
        return hello_service.say_hello(), 200
    else:  # POST
        json_data = request.get_json(silent=True)
        try:
            req_name, req_timestamp = parse_hello_json(json_data)
            hello_service.set_values(req_name, req_timestamp)
            return hello_service.say_hello(), 200
        except ValueError as err:
            return jsonify({'error': str(err)}), 400
