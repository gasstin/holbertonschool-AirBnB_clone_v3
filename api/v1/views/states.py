#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get__task():
    """Show States"""
    states = []
    for state in storage.all('State').values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get__task_id(state_id):
    """Get id of a task"""
    state_arr = storage.get('State', state_id)
    if state_arr is None:
        abort(404)
    else:
        return jsonify(state_arr.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def get__task_delete(state_id):
    """Delete task"""
    state_arr = storage.get('State', state_id)
    if state_arr is None:
        abort(404)
    else:
        storage.delete(state_arr)
        storage.save()
        return jsonify({}), 200

@app_views.route("/states", methods=['POST'], strict_slashes=False)
def set__task_POST():
    """Create a new object"""




@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def set__task_PUT(state_id):
    """ Updates a State object """