from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'devcontainers: Index Page'


@app.route('/hello')
def hello():
    return 'devcontainers: Hello, World'
