#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from main import app
from core import env
import controller


@app.route(env.rootpath + '/config/arcgis', methods=['GET', 'POST'])
def arcgisconfig():
    # GET METHOD
    method = request.method
    if (method == 'GET'):
        return controller.readArcgis()

    # POST METHOD
    elif(method == 'POST'):
        return controller.updateArcgis(request.get_json())


@app.route(env.rootpath  + '/config/basemap', methods=['GET', 'POST'])
def basemapconfig():
    # GET METHOD
    method = request.method
    if (method == 'GET'):
        return controller.readBasemap()

    # POST METHOD
    elif(method == 'POST'):
        return controller.updateBasemap(request.get_json())


@app.route(env.rootpath  + '/config/proxy', methods=['GET', 'POST'])
def proxyconfig():
    # GET METHOD
    method = request.method
    if (method == 'GET'):
        return controller.readProxy()

    # POST METHOD
    elif(method == 'POST'):
        return controller.updateProxy(request.get_json())


@app.route(env.rootpath  + '/config/secondpassword', methods=['POST', 'PUT'])
def secondpasswordconfig():
    # GET METHOD
    method = request.method
    if (method == 'PUT'):
        return controller.changePassword(request.get_json())

    # POST METHOD
    elif(method == 'POST'):
        return controller.loginPassword(request.get_json())


