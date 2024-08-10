from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    """Index page

    Returns:
        string: location string
    """
    return 'devcontainers: Index Page'


@app.route('/hello')
def hello():
    """Hello world page

    Returns:
        string: Hello world
    """
    return 'devcontainers: Hello, World'
