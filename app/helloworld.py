
from flask import jsonify
import datetime as dt


class HelloWorldService():

    def __init__(self):
        self.name = 'world'
        self.date = dt.datetime.now()

    def set_values(self, name: str, timestamp):
        self.name = name
        self.date = timestamp

    def say_hello(self):
        val = [
            {'message': 'Hello ' + self.name, 'time': self.date}
        ]
        return jsonify(json_data=val, status=200, mimetype='application/json')
