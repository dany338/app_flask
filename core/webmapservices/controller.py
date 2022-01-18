#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Doc."""
import json
import logging

from flask import jsonify
from owslib.wms import WebMapService

from ..database import db
from ..utils.utilities import Message 
from ..utils.utilities import ParamsRequired
from ..utils.jsonutilities import JsonUtilities

__author__ = 'Murphy Horta Camargo <murphy.camargo@senseta.com>'

TAG = "(Controller)"
PATHFILE = 'data/wms_list.json'
DB = JsonUtilities(PATHFILE)
################################################################
# Private
################################################################


def _required(val=None, param=""):
    if not val:
        raise ParamsRequired(param)


def _readWmsMetadata(link):
    layers = []
    print link
    wms = WebMapService(link, version='1.1.1')
    print wms.identification.title
    for layer in list(wms.contents):
        try:
            # Merge keywords of layer and wms
            keywords = wms[layer].keywords + wms.identification.keywords
            layers.append(dict({
                'name':       layer,
                'link':       link,
                'layertitle': wms[layer].title,
                'type':       wms.identification.type,
                'wmstitle':   wms.identification.title,
                'version':    wms.identification.version,
                'abstract':   wms.identification.abstract,
                'keywords':   keywords
            }))
        except Exception as e:
            print TAG + str(e.message)
            continue        
    return layers


def getMetadata(link):
    """Find out what a WMS has to offer. Service metadata."""
    try:
        data = _readWmsMetadata(link)
        return Message.successful(data=data)
    except Exception as e:
        return Message.failed(e=e)


def getEveryLayers():
    """Find out what a WMS has to offer. Service metadata."""
    try:
        data = db.getAllrecords()
        return Message.successful(data=data)
    except Exception as e:
        return Message.failed(e=e)


def getQuery(q):
    """Find out what a WMS has to offer. Service metadata."""
    try:
        print q
        data = db.search(q)
        return Message.successful(data=data)
    except Exception as e:
        return Message.failed(e=e)


def create(params):
    """Create a new layer into json file."""
    try:
        _required(params.get("url"), "url")
        _required(params.get("type"), "type")
        _required(params.get("nombre"), "nombre")
        _required(params.get("entidad"), "entidad")

        return jsonify({
            'ok': True,
            'message': 'WMS Created',
            'data': DB.insert(params)
        })
    except Exception as ex:
        return jsonify({
            'ok': False, 'message': ex.message, 'data': []
        })

def remove(params):
    """Remove a layer into json file."""
    try:
        _required(params["id"], "id")
        DB.remove(params)
        return jsonify({'ok': True, 'message': 'WMS Removed', 'data': params})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': []})

def read(params):
    """Return all records in the json file."""
    try:
        if not params.get("id"):
            return jsonify({'ok': True, 'data': DB.readAll()})
        else:
            return  jsonify({'ok': True, 'data': DB.readOne(params.get("id"))})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': []})

def update(params):
    """Remove a layer into json file."""
    try:
        _required(params["id"], "id")
        DB.update(params)
        return jsonify({'ok': True, 'message': 'WMS Update', 'data': params})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': []})


def importDocuments():
    """
    Import to data from Json.

    Get all wms from json file and insert it in database.
    Also return an Array of wms inserted.
    :return: `Wms list`
        `empty` otherwise
    :rtype: list
    """
    print TAG, "Start importing documents..."
    wms_imported = []
    layers_imported = 0
    with open(PATHFILE) as data_file:
        data = json.load(data_file)
        for obj in data:
            collection = []
            try:
                layers = _readWmsMetadata(obj["url"])
                for meta in layers:
                    layers_imported += 1
                    collection.append({
                        "code": obj["id"],
                        "name": meta["name"],
                        "link": meta["link"],
                        "type": meta["type"],
                        "wmstitle": meta["wmstitle"],
                        "layertitle": meta["layertitle"],
                        "entidad": obj["entidad"],
                        "version": meta["version"],
                        "abstract": meta["abstract"],
                        "keywords": meta["keywords"],
                    })
                wms_imported.append(obj)
                print "Insert for", len(collection)
                db.inserts(collection)
            except Exception as e:
                print TAG + str(e.message)
                
                continue
        print TAG, "Finish importing documents..."
        return {
            "WmsLength": len(wms_imported),
            "WmsImported": wms_imported,
            "LayersImported": layers_imported
        }


def updateDocuments():
    """Find out what a WMS has to offer. Service metadata."""
    try:
        print TAG, "Start updating documents..."
        db.removeAllrecords()
        print TAG, "Finish updating documents..."
        return Message.successful(data=importDocuments())
    except Exception as e:
        return Message.failed(e=e)
