#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from main import app, celery_app
from core import env
import controller
from ..utils.utilities import ParamsRequired

@app.route(env.rootpath + '/arcgis/geoprocessing', methods=['GET', 'POST', 'DELETE', 'PUT'])
def geoprecords():
    """DOC."""
    # GET METHOD
    method = request.method
    if (method == 'GET'):
        return controller.read(request.args)
     # POST METHOD
    elif(method == 'POST'):
        return controller.create(request.get_json())
    
    # PUT METHOD
    elif(method == 'PUT'):
        return controller.update(request.get_json())

    # REMOVE METHOD
    elif(method == 'DELETE'):
        return controller.remove(request.get_json())

@app.route(env.rootpath + '/arcgis/geoprocessing/handler', methods=['GET'])
def geophandler():
    """DOC."""
    # GET METHOD
    method = request.method
    if (method == 'GET'):
        required(request.args.get("action"), "action")

        if request.args.get("action") == True:
            celery_app.send_task('worker.geoprocess_schedule')
            return jsonify({ 'ok': True  'msg': "Celery worker started" })
        else:
            return updateStatus(1, False)
        


def required(val=None, param=""):
    if not val:
        raise ParamsRequired(param)