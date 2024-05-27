#!/usr/bin/python3
""" contains routes for the api"""

from api.v1.views import app_views
from flask import jsonify, redirect
from werkzeug.exceptions import NotFound
from models import storage


@app_views.route('/states')
def states():
    """return api status"""
    st = storage.all('State').values()
    all_states = [v.to_dict() for v in st]
    return jsonify(all_states)


@app_views.route('/states/<state_id>')
def get_state(state_id):
    """return api status"""
    st = storage.get('State', state_id)
    if st:
        return jsonify(st.to_dict())
    else:
        raise NotFound()
