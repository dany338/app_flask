#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main File"""

# Importing Flask package
from flask import Flask
# Set up CORS
from flask_cors import CORS
from celery import Celery

celery_app = Celery('worker', broker='amqp://guest@queue//')

app = Flask(__name__)
CORS(app)

# Setup app
from core.setup import *

if __name__ == '__main__':
    print("Running Main App")
    app.run(host='0.0.0.0', debug=True, port=80)
