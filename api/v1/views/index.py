#!/usr/bin/python3
""" to check the status """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ return the status of your API """
    return jsonify({'status': 'OK'})

@app_views.route('/stats')
def num_obj_bytype():
    """endpoint that retrives the number"""
    dic = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(dic)
