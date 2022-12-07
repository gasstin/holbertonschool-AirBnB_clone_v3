#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_task():
    """show all states"""
    states = []
    for state in storage.all('State').values():
        states.append(state.to_dict())
        return jsonify(states)
