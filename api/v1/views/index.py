#!/usr/bin/python3
""" contains routes for the api"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
# from models.amenity import Amenity
# from models.city import City
# from models.place import Place
# from models.review import Review
# from models.state import State
# from models.user import User


@app_views.route('/status')
def status():
    """return api status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type:"""
    al = storage.all()

    new = {}

    for k in al.keys():
        key = k.split('.')[0]
        if key not in new:
            new[key] = storage.count(key)

    return jsonify(new)
