#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, os, uuid
from core import env
from flask import jsonify
from werkzeug import secure_filename

def upload_file(_file):
    """Import a Temporal file."""
    checkFiles()
    _filename = secure_filename(_file.filename)
    _res_split = _filename.split(".")
    _extension = _res_split[1]
    _filenamecode = str(uuid.uuid4()) + "." + _extension
    _file.save(os.path.join(path_uploads, _filenamecode))
    return jsonify({
        'ok': True,
        'message': 'File was uploaded successfully ',
        'data': {"code": _filenamecode, "request_url": request.url}
    })

def checkFiles():
    """
    Check metadata of a file and remove it if  has expires.

    This function is called when a new file has uploaded.
    """
    NOW = time.time()
    print TAG, "Checking file"
    for f in os.listdir(env.path_uploads):
        # Create path file
        item_file = os.path.join(env.path_uploads, f)
        # Time of most recent content modification.
        modified_at = os.stat(item_file).st_mtime
        # Time which file will expires
        file_expires = modified_at + env.max_time
        if NOW > file_expires:
            print TAG, "Removing a file"
            os.remove(os.path.join(env.path_uploads, f))