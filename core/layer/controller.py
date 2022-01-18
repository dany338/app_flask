#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Doc."""
from flask import jsonify
from ..utils.utilities import ParamsRequired
from ..utils.jsonutilities import JsonUtilities

TAG = "(Layers)"
PATHFILE = 'data/privatelayers.json'
DB = JsonUtilities(PATHFILE)

__author__ = 'Murphy Horta Camargo <murphy.camargo@senseta.com>'


def _required(val=None, param=""):
    if not val:
        raise ParamsRequired(param)

def create(params):
    """Create a new layer into json file."""
    try:
        _required(params.get("type"), "type")
        _required(params.get("name"), "name")
        _required(params.get("group"), "group")
        _required(params.get("layer"), "layer")
        _required(params.get("url_wms"), "url_wms")
        _required(params.get("url_feature"), "url_feature")

        return jsonify({
            'ok': True,
            'message': 'Private layers added successfuly',
            'data': DB.insert({
                "type":         params.get("type"),
                "name":         params.get("name"),
                "group":        params.get("group"),
                "layer":        params.get("layer"),
                "url_wms":      params.get("url_wms"),
                "url_feature":  params.get("url_feature"),
                "url_legend":   params.get("url_wms")
                                + "request=GetLegendGraphic&"
                                + "version=1.3.0&format=image/png&"
                                + "layer=" + params.get("layer")
            })
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
        return jsonify({'ok': True, 'message': 'Private layer removed successfuly', 'data': params})
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
        return jsonify({'ok': True, 'message': 'Private layer edited successfuly', 'data': params})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': []})
