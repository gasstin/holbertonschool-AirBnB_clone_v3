#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Amenities"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/user', methods=['GET'], strict_slashes=False)
def get_user():
    """Retrieves the list of all User """
    all_user = storage.all(User).values()
    list_users = []
    for user in all_user:
        list_users.apppend(user.to_dict())
    return jsonify(list_users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """Retrieves a User object"""
    user_id = storage.get(User, user_id)
    if not user_id:
        abort(404)
    return jsonify(user_id.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user objetc"""
    all_useres = storage.get(User, user_id)
    if not all_useres:
        abort(404)
    storage.delete(all_useres)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>', methods=['POST'], strict_slashes=False)
def post_user(user_id):
    """Creates a User"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    request_user = request.get_json()
    instance_user = User(**request_user)
    instance_user.save()
    return make_response(jsonify(instance_user.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Update Users"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at', 'email']
    users =storage.get(User, user_id)
    if not users:
        abort(404)
    request_user = request.get_json()
    for key, value in request_user.items():
        if key not in ignore:
            setattr(users, key , value)
    storage.save()
    return make_response(jsonify(request_user.to_dict()), 200)
