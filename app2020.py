# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 09:45:40 2021

@author: G3
"""
import pandas as pd #version 1.1.5
import wiki_analysis
import plotly.express as px

import dash #version 1.19.0
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__) #start the app

#----------------------------------------------------------
# Importing data
wiki_es = wiki_analysis.Wiki_all_access("2020_es_wikidaily.csv", "latin1")
wiki_spanish = wiki_es.get_df()

#----------------------------------------------------------
# App Layout
app.layout = html.Div([
    
    html.H1 ("Wiki 2020", style={'text-align':'center'}),
    
    dcc.Dropdown(id="monat",
                 options=[
                     {"label":"All", "value":0},
                     {"label":"Ene", "value":1}, #label is what user sees, value is what is inside df variable
                     {"label":"Feb", "value":2},
                     {"label":"Mar", "value":3},
                     {"label":"Apr", "value":4},
                     {"label":"Mai", "value":5},
                     {"label":"Jun", "value":6},
                     {"label":"Jul", "value":7},
                     {"label":"Ago", "value":8},
                     {"label":"Sep", "value":9},
                     {"label":"Okt", "value":10},
                     {"label":"Nov", "value":11},
                     {"label":"Dez", "value":12}],
                 multi=False,
                 value=1,
                 style={'width':"40%"}
                 ),
    
    html.Div(id='output_container', children=[]),
    html.Br(),
    
    dcc.Graph(id='wiki_graph', figure={})
    
    ])

#----------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='wiki_graph', component_property='figure')],
    [Input(component_id='monat', component_property='value')]
    )

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    
    container = "The year chosen by user was: {}".format(option_slctd)
    
    wiki_spanish_pl = wiki_spanish.copy()
    
    if option_slctd != 0:
        wiki_spanish_pl = wiki_spanish[wiki_spanish_pl['month'] == option_slctd]
    
    wiki_spanish_pl = wiki_spanish_pl .rename(columns={'article':'Article',
                                                       'timestamp':'Date',
                                                       'total':'Views'})
    wiki_spanish_pl['Date'] = pd.to_datetime(wiki_spanish_pl['Date'], format='%Y%m%d%H')
    wiki_spanish_pl['Article'] = wiki_spanish_pl['Article'].str.replace('_',' ')
    
    fig = px.line(
        data_frame = wiki_spanish_pl,
        x='Date', 
        y='Views', 
        color='Article', 
        template='plotly_white') #hover_name='Article', hover_data=['Views']
    
    fig.update_layout(        
        title = ' Wikipedia for 2020',
        titlefont=dict(size=20,
                       color='#7f7f7f'),
        xaxis_title="",
        hoverlabel=dict(font_size=11), 
        hovermode='x',
        
        legend_title_text='Articles'
        )
    
    fig.update_traces(mode="lines", hovertemplate='Views: %{y:,.0f}')
    
    return container, fig

#----------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
