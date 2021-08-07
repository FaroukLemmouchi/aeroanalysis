#/bin/python
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

def figen_reflectance(reflectance, pixel, date):
    reflectance_fig = go.Figure()
    reflectance_fig.layout.title = f"Reflectance {pixel} {date}"
    pixrank = int(np.argwhere(reflectance["pixnum1"] == int(pixel)))
    
    reflectance_fig.add_trace(go.Scatter(x=reflectance["v_wavelength"][pixrank,:].data, y=reflectance["reflectance_meas"][pixrank,:].data, mode='lines', name='measured'))
    reflectance_fig.add_trace(go.Scatter(x=reflectance["v_wavelength"][pixrank,:].data,  y=reflectance["reflectance_sim"][pixrank,:].data, mode='lines', name='simulated'))
    reflectance_fig.add_trace(go.Scatter(x=reflectance["v_wavelength"][pixrank,:], y=reflectance["reflectance_meas"][pixrank,:] - reflectance["reflectance_sim"][pixrank,:], mode='markers', name='difference'))

    reflectance_fig.update_layout(uirevision=True,
            legend=dict(x=0.5, y=1.1, orientation='h'),
            title=dict(
                dict(font=dict(size=15)),x=0.1, y=0.9),
            margin=dict(l=0,b=60,t=60,r=0),
            xaxis=dict(uirevision=True,title='reflectance wavelength [nm]'),
            yaxis=dict(uirevision=True))
    return reflectance_fig 

def figen_profile(aod, pixel, title):
    profile_fig = go.Figure()
    profile_fig.layout.title = title
    ipix = np.where(aod['pixnum1'] == int(pixel))
    profile_fig.add_trace(go.Scatter(x=aod['aod_layer'][int(ipix[0]),:], y=np.arange(12), mode='lines', name='AOD vertical profile 550 nm'))
    profile_fig.update_layout(uirevision=True,
            legend=dict(x=0.5, y=1.1, orientation='h'),
            title=dict(
                dict(font=dict(size=15)),x=0.1, y=0.9),
            margin=dict(l=0,b=60,t=60,r=0),
            xaxis=dict(uirevision=True,title='AOD'),
            yaxis=dict(uirevision=True, title='Altitude [km]'))
    profile_fig.update_xaxes(range=[0, 0.5])
    return profile_fig


def figen_param(df, var, cmin=None, cmax=None):
    #param_fig = px.scatter_mapbox(df, lat='lat_centre', lon='lon_centre',color=var,
    #                        center=dict(lat=-25, lon=140), zoom=3, color_continuous_scale='jet',
    #                        mapbox_style='open-street-map')
    if var == "aerosol_optical_depth[550nm]":
      param_fig = go.FigureWidget(go.Scattermapbox( 
               lat=df['lat_centre'],
               lon=df['lon_centre'],
               mode='markers', 
               hovertext=list(zip(np.round(df[var], decimals=3), df['pixnum1'])),
               #hovertext= df['pixnum1'],
               #hoverinfo='lon+lat+text',
               
               marker=go.scattermapbox.Marker( 
                   cmin=cmin,
                   cmax=cmax,
                   opacity=0.3,
                   size=8, #4,
                   color=df[var],
                   colorscale="jet", #'ylorbr',
                   colorbar=dict(
               #       thicknessmode="pixels", thickness=30,
               #       lenmode="pixels", len=300,
               #       yanchor="top", y=1,
               #      ticks="outside", 
                      dtick=df[var].max()/10,
               ), 
           ),
      
      ))
    else :
      param_fig = go.FigureWidget(go.Scattermapbox( 
               lat=df['lat_centre'],
               lon=df['lon_centre'],
               mode='markers', 
               hovertext=list(zip(np.round(df[var], decimals=3), df['pixnum1'])),
               #hovertext= df['pixnum1'],
               #hoverinfo='lon+lat+text',
               
               marker=go.scattermapbox.Marker( 
                   cmin=cmin,
                   cmax=cmax,
                   opacity=0.3,
                   size=8, #4,
                   color=df[var],
                   colorscale='jet',
                   colorbar=dict(
               #       thicknessmode="pixels", thickness=30,
               #       lenmode="pixels", len=300,
               #       yanchor="top", y=1,
               #      ticks="outside", 
                      dtick=df[var].max()/10,
               ), 
           ),
      
      ))
    param_fig.update_layout( 
        uirevision=True, 
        margin=dict(l=0,b=20,t=0,r=0),
        autosize=True,
        hovermode='closest', 
        mapbox_style="open-street-map", 
        mapbox=dict(
        bearing=0,
        center=dict(
            lat=np.nanmean(df['lat_centre']),
            lon=np.nanmean(df['lon_centre']),
        ),
        pitch=0,
        zoom=4,
        ),
     )
    return param_fig


def figen_l1b(l1b, title):
    colors = ['green', 'orange','blue', 'red']
    l1b_fig = make_subplots(rows=3, cols=1, shared_xaxes=True, x_title='Wavelength [nm]')
    l1b_fig.update_layout(
            title = title,
            margin=dict(l=1,b=60,t=60,r=1),
            )
    for color, bd in zip(colors, l1b):
        l1b_fig.add_trace(go.Scatter(x=l1b[bd]['lambdas_rad'], y=l1b[bd]['rad'], name=bd, marker={'color':color}), row=1, col=1)
        l1b_fig.add_trace(go.Scatter(x=l1b[bd]['lambdas_irrad'], y=l1b[bd]['irrad'], showlegend=False, marker={'color':color}), row=2, col=1)
        l1b_fig.add_trace(go.Scatter(x=l1b[bd]['lambdas_rad'], y=(l1b[bd]['rad']/l1b[bd]['irrad']), showlegend=False, marker={'color':color} ), row=3, col=1)

        ##errors
        #l1b_fig.add_trace(go.Scatter(x=l1b[bd]['lambdas_rad'], y=l1b[bd]['rad_err'], name=f"{bd}_rad_err", showlegend=False, marker={'color':color}), row=4, col=1)
        #l1b_fig.add_trace(go.Scatter(x=l1b[bd]['lambdas_rad'], y=l1b[bd]['irrad_err'], name=f"{bd}_irrad_err", showlegend=False, marker={'color':color}), row=5, col=1)

    l1b_fig.update_layout(
            legend=dict(x=0.5, y=1.1, orientation='h'),
            title=dict(
                dict(font=dict(size=15)),x=0.1, y=0.9),
            )
    return l1b_fig

#def create_layers_fig(layer, xi, yi, volume, r, c):
#    layers_fig = go.Figure(go.Surface(x=xi, y=yi,
#        z=(0.1 + layer) * np.ones((r, c)),
#        surfacecolor=np.flipud(volume[layer]),
#        colorscale='jet',
#        opacity=0.3,
#        cmin=0, cmax=0.6,
#        #colorbar=dict(thickness=20, ticklen=4)
#        ))
#
#    layers_fig.update_layout(
#        width=1400,
#        height=600,
#        scene = dict(
#        aspectratio=dict(x=1, y=1, z=1),
#        xaxis = dict(
#            nticks=12, ticks='outside',
#            gridcolor="#f0f0f0",
#            title='Longitude',
#            backgroundcolor="white",
#            showbackground=False,
#            zerolinecolor="white",),
#        yaxis = dict(
#            gridcolor="#f0f0f0",
#            nticks=12, ticks='outside',
#            title='Latitude',
#            showbackground=False,
#            zerolinecolor="white"),
#        zaxis = dict(
#            gridcolor="#f0f0f0",
#            nticks=12, ticks='outside',
#            title='Altitude',
#            showbackground=False,
#            range=[-0.1, 12], autorange=False,
#            zerolinecolor="white",),),
#      )
#    return layers_fig
