#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from main import app
from core import env
import controller

@app.route(env.rootpath + '/weather', methods=['GET', 'POST', 'PUT', 'DELETE'])
def weahter():

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
