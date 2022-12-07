#!/usr/bin/python3
""" task 4 """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardownappcontext
def close_function(exit):
    storage.close()

@app.errorhandler(404)
def error_notfound(error):
    """returns a json-format 404 status"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'
    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    else:
        port = 5000
    app.run(port=port, host=host, threaded=True, debug=True)
