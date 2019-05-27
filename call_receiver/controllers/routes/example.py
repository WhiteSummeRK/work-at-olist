"""
WIP: Setting up one route for testing the project
"""

from flask import Blueprint, jsonify

app = Blueprint('example', __name__)


@app.route('/')
def example_route():
    return jsonify({'State': 'Success'})
