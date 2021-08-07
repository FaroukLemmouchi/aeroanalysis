#/bin/python
import dash, os, glob, sys
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from aeros5p_analysis.aeros5py_reader import read_l1b 
from aeros5p_analysis.fig_generator import *
import plotly.graph_objects as go

from aeros5p_analysis.index import dash_app, session_id, conf
from aeros5p_analysis.utils import get_data_locally, save_paths, load_paths

pix_list = []

from aeros5p_analysis.layouts import l1b, aod

globals()['aod_tmp'] = aod

#dash_app.config.suppress_callback_exceptions = True

@dash_app.callback(
        [Output('pixel0', 'value'),
         Output('param-map', 'figure')],
        [Input('reload-data', 'n_clicks'),
         Input('var-selector', 'value')],
        [State('root', 'value'), State('date', 'value'), State('simulation', 'value'), State('pixel0', 'value')])

def reload(clicks, var, root_path, date, simulation, pixel) :
    l1b, aod = get_data_locally(session_id, root_path=root_path, date=date, simulation=simulation, pixel=pixel)
    globals()['aod_tmp'] = aod
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] == 'reload-data.n_clicks' :
        tmp =  {"simulation":simulation, "date":date, 'root_path':root_path}
        save_paths( 'current_config.yaml' , mode='CURRENT', **tmp)
        try :
          l1b = read_l1b(l1b_file) 
          l1b_fig = figen_l1b(l1b, title=l1b_file.split('/')[-1])
          reflectance_fig = figen_reflectance(aod, pixel, date) 
        except :
          pass
        
        if var in aod.keys():
            param_fig = figen_param(aod, var, conf['vlim'][var][0], conf['vlim'][var][1]) 
        else :
            param_fig = figen_param(aod, var)
        return str(pixel), param_fig 

    elif ctx.triggered[0]['prop_id'] == 'var-selector.value' :
        if var in aod.keys():
            param_fig = figen_param(aod, var, conf['vlim'][var][0], conf['vlim'][var][1]) 
        else :
            param_fig = figen_param(aod, var)
        return str(pixel), param_fig
    return str(pixel), go.FigureWidget()


@dash_app.callback(
        [Output('l1b-graph', 'figure'),
        Output('reflectance-graph', 'figure'), #],
        Output('profile-graph', 'figure')],
        [Input('update', 'n_clicks'), Input('pixel0', 'value')],
        [State('root', 'value'), State('date', 'value'), State('simulation', 'value')])
def update_graphs(clicks, pixel, root_path, date, simulation):
    if pixel == '' or not pixel.isdigit() : raise PreventUpdate()
    l1b_file =f"{root_path}/INPUTS/{date}/GOME2_data/S5P_L1B_4ch_{date}_{str(pixel)}.dat" 
    l1b_fig, reflectance_fig, profile_fig = go.Figure(), go.Figure(), go.Figure()

    try :
      l1b = read_l1b(l1b_file) 
      l1b_fig = figen_l1b(l1b, title=l1b_file.split('/')[-1])
      reflectance_fig = figen_reflectance(aod, pixel, date) 
      profile_fig = figen_profile(aod_tmp, pixel, title=f'{pixel} AOD profile')
    except :
      pass
    return l1b_fig , reflectance_fig, profile_fig


@dash_app.callback( 
            Output('pixels-list', 'children'),
            [Input('param-map','clickData'),
             Input('reset', 'n_clicks'),
             Input('dump-pixels', 'n_clicks')],
            [State('pixels-list', 'children'),
             State('root', 'value'), State('date', 'value'), State('simulation', 'value')])
def append_pixel(clickData, n_clicks, dump_clicks, pix_list_str,  root_path, date, simulation):
    if pix_list_str is None : 
        pix_list = list()
    else :
        pix_list = eval(pix_list_str)
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] == 'reset.n_clicks' : 
        pix_list = []
        return str(pix_list)
    elif ctx.triggered[0]['prop_id'] == 'dump-pixels.n_clicks' :
        pix_list = set(pix_list) ; pix_list = list(pix_list) #remove dups
        with open(f'pixels.csv', 'w') as f :
          pix_list = list(dict.fromkeys(pix_list))
          f.write('       '.join(np.asarray(pix_list, dtype=str)))
        return str(pix_list) 

    elif ctx.triggered[0]['prop_id'] == 'param-map.clickData':
        npix = clickData['points'] #list of dicts
        for i in npix:
            try :
                pix_list.append(aod_tmp['pixnum1'][i['pointIndex']]) # warning global var
            except :
                try :
                    pix_list.append(aod_tmp['pixnum1'][i['pointIndex']]) # warning global var
                except :
                    pix_list.append('error')
        return str(pix_list)


@dash_app.callback(
        Output('dummy-div', 'children'),
        [Input('clear-cache', 'n_clicks'),
         Input('remove-extracted', 'n_clicks')])
def clean_trash(cache_clicks, remove_clicks ):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] == 'clear-cache.n_clicks' :
        [os.remove(f) for f in glob.glob('cache-directory/*')]
        return str('ok') #Cache cleared') #Not implemented (clear cache)')
