#!/usr/bin/python3
""" contains routes for the api"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/states')
def states():
    """return api status"""
    st = storage.all('State').values()
    all_states = [v.to_dict() for v in st]
    return jsonify(all_states)
