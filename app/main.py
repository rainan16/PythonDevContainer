from flask import Flask, request
from helloworld import HelloWorldService

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Index page

    Returns:
        string: location string
    """
    return 'devcontainers: Index Page'


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    """Hello world page (POST and GET)

    Returns:
        string: A hello string
    """
    if request.method == 'GET':
        return HelloWorldService().say_hello()
    elif request.method == 'POST':
        json_data = request.get_json(silent=True)
        try:
            req_name, req_timestamp = parse_hello_json(json_data)
        except ValueError as err:
            return str(err), 400
        hello_service = HelloWorldService()
        hello_service.set_values(req_name, req_timestamp)
        return hello_service.say_hello()
    else:
        return "", 500


def parse_hello_json(json_data):
    if not json_data:
        raise ValueError("Must provide JSON")

    try:
        req_name: str = json_data['name']
        req_timestamp = json_data['timestamp']
    except KeyError as err:
        raise ValueError(
            "Must provide JSON with name and timestamp (missing: {b1})"
            .format(b1=err)
        )

    return req_name, req_timestamp
