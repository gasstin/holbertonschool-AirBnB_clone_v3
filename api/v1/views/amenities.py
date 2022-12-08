#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Amenities"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amentities(amenities_id):
    """Retrieves a list of all amenities"""
    all_amenities = storage.all(Amenity).values()
    amenities_list = []
    for amenity in all_amenities:
        amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenities_id):
    """"" Retrieves an amenity """
    amenities_get = storage.get(Amenity, amenities_id)
    if not amenities_get:
        abort(404)
    else:
        return jsonify(amenities_get.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an amenity  Object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def post_amenities(amenities_id):
    """"creates amenities"""
    if not request.get_json():
        abort(404, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(404 , description="Missing name")
    request_data = request.get_json()
    instance = Amenity(**request_data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenities(amenities_id):
    """update amenities"""
    amenities_all = storage.get(Amenity, amenities_id)
    if not amenities_all:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    data_amenities = request.get_json()
    for key, value in data_amenities.items():
        if key not in ignore:
            setattr(amenities_all, key, value)
        storage.save()
    return make_response(jsonify(amenities_all.to_dict()), 200)
    