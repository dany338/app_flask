#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from main import app
from core import env
import controller

@app.route(env.rootpath + '/layers', methods=['GET', 'POST', 'PUT', 'DELETE'])
def layers():
    """DOC."""
    # GET METHOD
    method = request.method
    if (method == 'GET'):
        return controller.read(request.args)

    # POST METHOD
    elif(method == 'POST'):
        print request.get_json()
        return controller.create(request.get_json())
    
    # PUT METHOD
    elif(method == 'PUT'):
        print request.get_json()
        return controller.update(request.get_json())

    # REMOVE METHOD
    elif(method == 'DELETE'):
        print request.json
        return controller.remove(request.get_json())
