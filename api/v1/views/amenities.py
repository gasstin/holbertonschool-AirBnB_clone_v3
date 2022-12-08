#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Amenities"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/amenities/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amentities(amenities_id):
    """Retrieves a list of all amenities"""
    all_amenities = storage.all(Amenity).values()
    amenities_list = []
    for amenity in all_amenities:
        amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list)
