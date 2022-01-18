"""This module has everythings to setup Solr database."""
# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys, datetime, json, logging
from flask import jsonify
import urllib, json, time
from ..core.utils.utilities import ParamsRequired
from ..core.utils.jsonutilities import JsonUtilities

__author__ = 'Murphy Horta Camargo <murphy.camargo@senseta.com>'

# TAG {string}: Used to identify the source of a log message.
# It usually identifies the class or controller where the log call occurs.
# e.g  print TAG, message
TAG = "(Arcgis)"
PATHFILE = 'data/warmap.json'
DB = JsonUtilities(PATHFILE)

# https://cscfjina.cfjcs.net/server/rest/services/cerebro_gp/BufferPolygon/GPServer/BufferPolygon/submitJob

class GeoprocessTask:

    def __init__(self, serviceUrl, taskUrl):
        """Doc."""
        self.serviceUrl = serviceUrl
        self.submitUrl  = serviceUrl + "/GPServer/{0}/submitJob/".format(taskUrl)
        self.jobUrl     = serviceUrl + "/GPServer/{0}/jobs/".format(taskUrl)
        self.resultUrl  = serviceUrl + "/MapServer/jobs/"
    

    def runTask(self, params):
        self.submitResponse = urllib.urlopen(self.submitUrl, urllib.urlencode(params))   
        self.submitJson = json.loads(submitResponse.read())

        if 'jobId' in self.submitJson:

            self.jobID  = self.submitJson['jobId']        
            self.status = self.submitJson['jobStatus']        
            self.jobUrl = self.jobUrl + self.jobID
            self.checkJobResponse(self, self.status)
                                                
        else:
            print ("no jobId found in the response")


    def checkJobResponse(self, status):

        while status == "esriJobSubmitted" or status == "esriJobExecuting":
            print "checking to see if job is completed..."
            print status
            time.sleep(1)
            
            jobResponse = urllib.urlopen(self.jobUrl, "f=json")     
            jobJson = json.loads(jobResponse.read())
        
            if 'jobStatus' in jobJson:
                status = jobJson['jobStatus']
            
                if status == "esriJobSucceeded":
                    DB.insert({
                        url: self.resultUrl,
                        time:  datetime.datetime.now()
                    })                    
                if status == "esriJobFailed":                                        
                    if 'messages' in jobJson:                        
                        print jobJson['messages']
