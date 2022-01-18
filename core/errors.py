#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main import app

@app.errorhandler(404)
def page_not_found(error):
    """Doc."""
    return '<h1 align="center">The server respond 404 Page Not Found.</h1>'

