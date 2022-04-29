from dash import Dash, html, Input, Output, dcc
import dash_bootstrap_components as dbc
from app import dash_app
import plotly.express as px
from data_dummy import DataDummy
from app import dash_app
import pandas as pd
from math import ceil
import numpy as np
import pdb

dash_app.title = 'Dashboard | Live prices'
layout = html.Div([html.H1('Crypto Dashboard',className='header',id='page'),\
                   html.Br(),\
                   html.Div(children=[],id='page_content_live_prices')])

@dash_app.callback(
    Output(component_id='page_content_live_prices',component_property='children'),
    Input(component_id='url',component_property='pathname')
)
def update_live_prices(pathname):
    data_dummy_obj = DataDummy()
    query = 'SELECT * FROM dummy_data WHERE indicator = "close";'
    df = pd.read_sql(sql=query, \
                     con=data_dummy_obj.dummy_conn_obj, \
                     index_col='date').drop(['index'], axis=1).drop('indicator', axis=1).reset_index(False)
    assets = df['ticker'].unique().tolist()
    container_all_cards_ls = []
    if len(assets)%3!=0:
        nrow = ceil(len(assets)/3)
        print('nrow is %s' %nrow)
    else:
        nrow = len(assets)
    # Trick to get the asset names into the same grid shape as the page layout
    assets_grid = assets[::]
    # Fill any gap to make the list reshapable by nx3 grid
    assets_grid = assets_grid + (3 - nrow) * [None]
    assets_grid = np.reshape(assets_grid, (nrow, 3))
    temp_child_ls = []
    for i in range(0,nrow):
        for j in range(0,3):
            if assets_grid[i,j] is None:
                break
            else:
                temp_child_ls.append(\
                    dbc.Row(\
                        children=[\
                            dbc.Col(\
                                children=\
                                    dbc.Card(\
                                        children=\
                                            [dbc.CardBody(\
                                                children=[dbc.Row(children=[dbc.Col(children=[assets_grid[i,j],\
                                                                                              html.P('Change 1D')])]),\
                                                          dbc.Row(children=[dbc.Col(children=[])])])]))]))
        new_children = dbc.Container(children=temp_child_ls)
    return new_children