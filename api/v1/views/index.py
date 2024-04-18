#!/usr/bin/python3
"""
Create a new state object handling default
RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def get_status():
    """Returns a JSON status response."""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stats():
    """Retrieves the number of each type of object by type."""
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    stats = {cls: storage.count(obj) for cls, obj in classes.items()}
    return jsonify(stats)
