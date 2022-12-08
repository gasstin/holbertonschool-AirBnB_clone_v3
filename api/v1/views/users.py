#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Amenities"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    """
    Retrieves a list of all users
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<users_id>/', methods=['GET'], strict_slashes=False)
def get_user(users_id):
    """ Retrieves an users """
    users_get = storage.get(User, users_id)
    if not users_get:
        abort(404)

    return jsonify(users_get.to_dict())


@app_views.route('/users/<users_id>', methods=['DELETE'], strict_slashes=False)
def delete_users(users_id):
    """
    Deletes an users  Object
    """
    us_er = storage.get(User, users_id)
    if not us_er:
        abort(404)
    storage.delete(us_er)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """
    Creates an users
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    request_user = request.get_json()
    instance = User(**request_user)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<users_id>', methods=['PUT'], strict_slashes=False)
def put_users(users_id):
    """
    Updates an user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at', 'email']
    us_er = storage.get(User, users_id)
    if not us_er:
        abort(404)
    request_users = request.get_json()
    for key, value in request_users.items():
        if key not in ignore:
            setattr(us_er, key, value)
    storage.save()
    return make_response(jsonify(us_er.to_dict()), 200)
