import os
from main import app
from flask import send_file

from core.webmapservices.routes import *
from core.basemaps.routes import *
from core.weather.routes import *
from core.config.routes import *
from core.layer.routes import *
from core.errors import *

from core import env


# Api Welcome page
# Root Path
@app.route(env.rootpath + '/', methods=['GET'])
def welcome():
    return send_file('templates/welcome.html')

# Without any route, redirect to frontend's index file
@app.route('/',  methods=['GET'])
def index():
    return send_file(env.path_frontend + 'index.html')

# Everything not declared before (not an API route)
# should be handled by Angular2 and its static files
@app.route('/<path:path>')
def route_frontend(path):
    file_path = env.path_frontend + path
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        return send_file(env.path_frontend + 'index.html')


@app.before_first_request
def setup():
    _writeFile(env.path_uploads)


def _writeFile(directory):
    """Create a folder if not exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)






