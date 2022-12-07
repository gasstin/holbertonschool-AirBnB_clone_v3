#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from flask import Flask, jsonify, abort, request
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

@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get__task_id(state_id):
    """get states id"""
    state_permision = storage.get('State', state_id)
    if state_permision is None:
        abort(404)
    else:
        return jsonify(state_permision.to_dict())

@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def get__task_delete(state_id):
    """delete task"""
    state_permision = storage.get('State', state_id)
    if state_permision is None:
        abort(404)
    else:
        storage.delete(state_permision)
        storage.save()
        return jsonify({}), 200