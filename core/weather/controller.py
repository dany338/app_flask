#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Doc."""
import json
import logging
from flask import jsonify

from ..utils.utilities import Message 
from ..utils.utilities import ParamsRequired
from ..utils.jsonutilities import JsonUtilities

TAG = "(Weather)"
PATHFILE = 'data/weatherlayers.json'
DB = JsonUtilities(PATHFILE)


__author__ = 'Murphy Horta Camargo <murphy.camargo@senseta.com>'


def _required(val=None, param=""):
    if not val:
        raise ParamsRequired(param)

def create(params):
    """Create a new layer into json file."""
    try:
        _required(params.get("url"), "url")
        _required(params.get("type"), "type")
        _required(params.get("name"), "name")
        _required(params.get("minZoom"), "minZoom")
        _required(params.get("maxZoom"), "maxZoom")
        _required(params.get("attribution"), "attribution")

        return jsonify({
            'ok': True,
            'message': 'Weather Created',
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
        return jsonify({'ok': True, 'message': 'Weather Removed', 'data': params})
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
        return jsonify({'ok': True, 'message': 'Basemap Updated', 'data': params})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': []})
