#!/usr/bin/python3
"""flask entry point"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """closes storage"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    '''This method handles the 404 HTTP error'''
    return (jsonify(error='Not found'), 404)


@app.errorhandler(400)
def error_400(error):
    '''Handles 400 HTTP error code.'''
    msg = "Bad request"
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return (jsonify(error=msg), 400)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
