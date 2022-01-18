"""This file has a class to access a json files"""
# -*- coding: utf-8 -*-
# !/usr/bin/env python

import json
import sys
import logging
from flask import jsonify

__author__ = 'Murphy Horta Camargo <murphy.camargo@senseta.com>'

# TAG {string}: Used to identify the source of a log message.
# It usually identifies the class or controller where the log call occurs.
# e.g  print TAG, message
TAG = "(Json Utilities)"

class JsonUtilities:
    """This class has all functions [READ - UPDATE - REMOVE - DELETE ... ] objects from a json file"""

    def __init__(self, targetfile):
        """Doc."""
        self.PATHFILE = targetfile
        print "Target file {0}".format(targetfile)



    def autoIncrement(self, _property, _list):
        max_id = 0
        for item in _list:
            if int(item[_property]) > max_id:
                max_id = int(item[_property])
        max_id += 1
        return str(max_id)

    def readAll(self):
        with open(self.PATHFILE, 'r+') as f:
            return json.load(f)

    def readOne(self, code):
        result = None
        with open(self.PATHFILE, 'r+') as f:
            result = list(filter(lambda x: x['id'] == code, json.load(f)))
            if len(result) > 0:
                return result[0]
            else:
                return None

    def updateUtil(self, x, y):
        if x['id'] == y['id']:
            return y
        else:
            return x

    def update(self, object):
        result = None
        with open(self.PATHFILE, 'r+') as f:
            result = map(lambda x: self.updateUtil(x, object), json.load(f))
            f.seek(0)
            json.dump(result, f, indent=4)
            f.truncate()
            return result
    
    def remove(self, object):
        result = None
        with open(self.PATHFILE, 'r+') as f:
            result = filter(lambda x: x['id'] != object['id'], json.load(f))
            f.seek(0)
            json.dump(result, f, indent=4)
            f.truncate()
            return result
    
    def insert(self, object):
        result = None
        with open(self.PATHFILE, 'r+') as f:
            result = json.load(f)
            object['id'] = self.autoIncrement("id", result)
            result.append(object)
            f.seek(0)
            json.dump(result, f, indent=4)
            f.truncate()
            return result
            
    