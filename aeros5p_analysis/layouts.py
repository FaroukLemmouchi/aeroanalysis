#!/bin/python

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from aeros5p_analysis.index import session_id, mode

from aeros5p_analysis.utils import load_paths

from aeros5p_analysis.utils import get_data_locally, load_paths
conf = load_paths('config.yaml', mode)

l1b, aod = get_data_locally(session_id, **conf)


param_fig = go.Figure()  
l1b_fig = go.FigureWidget() 
reflectance_fig = go.FigureWidget() 
profile_fig = go.FigureWidget()

layout = html.Div(id="main", children=[
    html.Div(id='dummy-div'),
    html.H1(children='~~~ Retrieval Analysis ~~~', style={'textAlign':'center'}),
    html.Div(id='str-saver'),
    html.Br(),
    html.Div([
    html.Button('Reload data', id='reload-data', style={'margin':'14px'}),
    html.Button('Clear cache', id='clear-cache', style={'margin':'14px'}),
    html.Br(),
    html.Button('Remove local files', id='remove-extracted', style={'margin':'14px'}),
    html.Br(),
    ], style={'columnCount':'3'}),
    html.Div([
    html.Label('Region root path '),#, style={'margin': "10px" , 'textAlign':'center'}),
    html.Br(),
    dcc.Input(id='root',value=conf['root_path'], type='text'),
    html.Br(),
    html.Label('Date'),#, style={'margin': "10px" , 'textAlign':'center'}),
    html.Br(),
    dcc.Input(id='date', type='text', value=conf['date']),
    html.Br(),
    html.Label('Simulation'),
    html.Br(),
    dcc.Input(id='simulation', value=conf['simulation']),
    html.Br(),
    ], style={'columnCount':'3'}),
    html.Br(),
    html.Div([
    dcc.Dropdown(id='var-selector',
        options=[ dict(
            label=var, value=var,
        ) for var in ['aerosol_optical_depth[550nm]', 'cloud_fraction', 'surface_height', 'viirs_cloud_mask', 'totcol']
        ],
        value='aerosol_optical_depth[550nm]'
        ),
    dcc.Graph(id='param-map', figure=param_fig),
    ]),
    dcc.Input(id='pixel0', value='', debounce=True, placeholder="Past pixel id here"),
    html.Button('Update', id='update'), 
    html.Button('Reset', id='reset'), 
    html.Button('Dump', id='dump-pixels'), 
    html.Br(),
    html.Div([ 
        html.Label('Selected pixels:'),
        html.Div(id='pixels-list'),
        ]),
    html.Br(),
    html.Div([
        dcc.Graph(id='reflectance-graph', figure=reflectance_fig),
        dcc.Graph(id='profile-graph', figure=profile_fig), 
    ], style={'columnCount':'2'}),
    html.Div([
    dcc.Graph(id='l1b-graph', figure=l1b_fig),]),
    html.Div(['E-mail: farouk.lemmouchi@lisa.u-pec.fr (2020)'], style={'textAlign':'right'}),
])
