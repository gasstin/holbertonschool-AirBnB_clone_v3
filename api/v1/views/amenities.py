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
        return jsonify(amenities_get.to_dict)
