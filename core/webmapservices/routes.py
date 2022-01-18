#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, send_file
from main import app
from core import env
import controller


""" @app.before_first_request
def setup():
    controller.updateDocuments() """



@app.route(env.rootpath + '/webmapservice', methods=['GET', 'POST', 'PUT', 'DELETE'])
def webmapservice():
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


@app.route(env.rootpath + '/webmapservice/solr', methods=['GET', 'PUT'])
def wms():
    """DOC."""
    # GET METHOD
    method = request.method
    if (method == 'GET'):
        if "layers" in request.args:
            return controller.getEveryLayers()
        elif "q" in request.args:
            q = request.args.get("q")
            return controller.getQuery(q)
        else:
            return controller.getEveryLayers()
    # PUT METHOD
    elif(method == 'PUT'):
        return controller.updateDocuments()

@app.route(env.rootpath + '/webmapservice/metadata', methods=['POST'])
def wmsmetadata():
    """
    Get all wms from database. If there isn't wms return a empty array.

    :return: `Wms list`
        `empty` otherwise
    :rtype: list
    """
    link = None
    if "link" in request.json:
        link = request.json["link"]
    return controller.getMetadata(link)

