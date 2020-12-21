"""A basic flask applications"""
import os
from flask import Flask
from flask import Response
from flask import json

app = Flask(__name__)

@app.route('/')
def index():
    """Index page of the application."""
    return "Hello, World! (from a Docker container)"

@app.route('/cities.json')
def cities():
    """A JSON formatted result."""
    data = ["Amsterdam", "San Francisco", "Berlin", "New York"]
    resp = Response(json.dumps(data), status=200, mimetype="application/json")
    return resp

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
