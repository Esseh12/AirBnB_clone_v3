#!/usr/bin/python3
""" contains routes for the api"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """return api status"""
    return jsonify({"status": "OK"})
