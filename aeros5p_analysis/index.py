#!/bin/python
# -*- coding: utf-8 -*-
import dash
import sys

mode = "DEMO" #SEE main.py 

from flask_caching import Cache
from flask import Flask 
server = Flask(__name__)
dash_app = dash.Dash(__name__, server=server, url_base_pathname='/')#, external_stylesheets=external_stylesheets)

@server.route("/")
def my_dash_app():
    return dash_app.index()

cache = Cache(dash_app.server, config={
'CACHE_TYPE': 'redis',
# Note that filesystem cache doesn't work on systems with ephemeral
# filesystems like Heroku.
'CACHE_TYPE': 'filesystem',
'CACHE_DIR': 'cache-directory',

# should be equal to maximum number of users on the app at a single time
# higher numbers will store more data in the filesystem / redis cache
'CACHE_THRESHOLD': 200
})


import uuid
session_id = str(uuid.uuid4())
from aeros5p_analysis.utils import load_paths, save_paths

#root_path, date, simulation, pixel , var = load_paths('paths.config', mode)
conf = load_paths('config.yaml', mode)

save_paths(config_file='current_config.yaml', mode='CURRENT', **conf)

from aeros5p_analysis import callbacks
from aeros5p_analysis.layouts import layout
dash_app.layout = layout 

#dash_app.index_string = """
#<!DOCTYPE html>
#<html>
#    <head>
#        {%metas%}
#        <title>AEROS5P</title>
#        {%favicon%}
#        {%css%}
#    </head>
#    <body>
#        {%app_entry%}
#        <footer>
#            {%config%}
#            {%scripts%}
#            {%renderer%}
#        </footer>
#    </body>
#</html>
#"""

