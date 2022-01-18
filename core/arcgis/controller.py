# -*- coding: utf-8 -*-
"""Doc."""
from flask import jsonify
from ..utils.utilities import ParamsRequired
from ..utils.jsonutilities import JsonUtilities

TAG = "(Arcgis Controller)"
    PATHFILE = 'data/geoprocess.json'
DB = JsonUtilities(PATHFILE)

__author__ = 'Murphy Horta Camargo <murphy.camargo@senseta.com>'


def _required(val=None, param=""):
    if not val:
        raise ParamsRequired(param)

def create(params):
    """Create a new layer into json file."""
    try:
        _required(params.get("service"), "service")
        _required(params.get("task"), "task")
        _required(params.get("every"), "every")
        return jsonify({
            'ok': True,
            'message': 'Geoprocess Created',
            'data': DB.insert(params)
        })
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': []})


def remove(params):
    """Remove a layer into json file."""
    try:
        _required(params["id"], "id")
        DB.remove(params)
        return jsonify({'ok': True, 'message': 'Geoprocess Removed', 'data': params})
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
        return jsonify({'ok': True, 'message': 'Geoprocess Updated', 'data': params})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': []})


def updateStatus(id, status):
    """Remove a layer into json file."""
    try:
        result = DB.readOne(id)
        result.status = status
        DB.update(result)
        return jsonify({'ok': True, 'message': 'Status Updated', 'data': result})
    except Exception as ex:
        return jsonify({'ok': False, 'message': ex.message, 'data': []})



