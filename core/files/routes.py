#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, send_file, jsonify
from main import app
from core import env
import controller
import time


@app.before_first_request
def setup():
    controller.checkFiles()


@app.route(env.rootpath + '/uploads/<id>')
def data(id):
    """Doc."""
    return send_file(env.path_uploads + str(id))


@app.route(env.rootpath + '/uploads', methods=['POST'])
def gpRlMarkerLine():
    """Import a Temporal file."""
    if 'file' not in request.files:
        return jsonify({
            'ok': False,
            'data': str(request.url),
            'message': 'Something has happened. The server is not receiving the file. Check your file or headers'
        })
    else :
        _file = request.files['file']
        return controller.upload_file(_file)

