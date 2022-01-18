#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Doc."""
import json
from flask import jsonify
from ..utils.utilities import ParamsRequired
from ..utils.jsonutilities import JsonUtilities

# TAG {string}: Used to identify the source of a log message.
# It usually identifies the class or controller where the log call occurs.
# e.g  print TAG, message
TAG = "(Config)"
# @const path_privatelayer : String
# It's used to indicate the path of privatelayers
PATHFILE = 'data/config.json'
# @const path_privatelayer : String
# It's used to indicate the path of privatelayers
PRIVATE_LAYER_PATH = "data/privatelayers.json"

__author__ = 'Murphy Horta Camargo <murphy.camargo@senseta.com>'


def _required(val=None, param=""):
    if not val:
        raise ParamsRequired(param)


def _getField(field):
    with open(PATHFILE, 'r+') as f:
        data = json.load(f)
        if data[field]:
            return data[field]
        else:
            print "Failed getting {0} in configuration file".format(field)
            raise Exception('Failed getting configuration file.')

def _setField(field, value):
    with open(PATHFILE, 'r+') as f:
        data = json.load(f)
        if data[field]:
            data[field] = value
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            return True
        else:
            print "Field {0} doesn't exist on file".format(field)
            raise Exception('Failed setting configuration file.')


def _updatePrivateLayers(oldhost, newhost):
    with open(PRIVATE_LAYER_PATH, 'r') as file:
        filedata = file.read()    
    
    print oldhost
    print newhost
    filedata = filedata.replace(oldhost, newhost)

    with open(PRIVATE_LAYER_PATH, 'w') as file:
        file.write(filedata)


def readBasemap():
    """Get basemap from file"""
    try:
        return jsonify({'ok': True, 'message': 'Basemap by default', 'data': _getField('BASEMAP')})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': None})

def updateBasemap(params):
    """Set basemap from file"""
    try:
        return jsonify({'ok': True, 'message': 'Basemap', 'data': _setField('BASEMAP', params.get("name"))})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': None})

def readArcgis():
    """Get basemap from file"""
    try:
        return jsonify({'ok': True, 'message': 'Arcgis Host', 'data': _getField('ARCGISHOST')})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': None})

def updateArcgis(params):
    """Set basemap from file"""
    try:
        newH = params.get("host")
        oldH = _getField('ARCGISHOST')

        _setField('ARCGISHOST', params.get("host"))
        _updatePrivateLayers(oldH, newH)

        return jsonify({'ok': True, 'message': 'Arcgis Changed', 'data': True})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': None})

def readProxy():
    """Get proxy from file"""
    try:
        return jsonify({'ok': True, 'message': 'Url proxy', 'data': _getField('PROXY')})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': None})

def updateProxy(params):
    """Set proxy from file"""
    try:
        return jsonify({'ok': True, 'message': 'proxy updated', 'data': _setField('PROXY', params)})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': None})

def changePassword(params):
    """Change second password"""
    try:
        _required(params.get("old"), "old")
        _required(params.get("new"), "new")

        if _getField('PASSWORD') != params.get("old"):
            raise Exception('La contraseña actual no coincide con la ingresada.')
       
        _setField('PASSWORD', (params.get("new")))

        return jsonify({'ok': True, 'message': 'Second Password changed', 'data': True})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': None})


def loginPassword(params):
    """Login second password"""
    try:       
        _required(params.get("password"), "password")

        if _getField('PASSWORD') != params.get("password"):
            raise Exception('La contraseña actual no coincide con la ingresada.')

        return jsonify({'ok': True, 'message': 'Second Password login', 'data': True})

    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': None})
