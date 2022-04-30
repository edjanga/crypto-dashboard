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
layout = html.Div([html.H1(children=[html.B('Tech Stock Dashboard')],className='header',id='page'),\
                   html.Br(),\
                   dcc.Interval(id='interval-component',interval=60*60*1000),\
                   html.Div(children=[],id='page_content_live_prices')])

@dash_app.callback(
    Output(component_id='page_content_live_prices',component_property='children'),
    [Input(component_id='interval-component', component_property='n_intervals'),\
     Input(component_id='url',component_property='pathname')]
)
def update_live_prices(n,pathname):
    data_dummy_obj = DataDummy()
    query = 'SELECT * FROM dummy_data WHERE indicator = "close";'
    df = pd.read_sql(sql=query, \
                     con=data_dummy_obj.dummy_conn_obj, \
                     index_col='date').drop(['index'], axis=1).drop('indicator', axis=1).reset_index(False)
    query = ''
    assets = df['ticker'].unique().tolist()
    for index, asset in enumerate(assets):
        if index == len(assets) - 1:
            query = ','.join((query, ''.join((r'"%s"' % asset, ')'))))
        elif index == 0:
            query = ''.join((query, '(', r'"%s"' % asset))
        else:
            query = ','.join((query, r'"%s"' % asset))
    query = ' '.join(('SELECT * FROM dummy_data WHERE ticker in', query, 'AND indicator = "close";'))
    df = pd.read_sql(sql=query, \
                     con=data_dummy_obj.dummy_conn_obj,\
                     index_col='date').drop(['index'],axis=1).drop('indicator',axis=1).reset_index(False)
    # Unmelt data then calculate returns
    df = pd.pivot_table(df,values='price',index='date',columns='ticker')
    df = df.loc[:,df.columns.isin(assets)]
    df = df.ffill()
    first_date = df.apply(pd.Series.first_valid_index).sort_values(ascending=False)[0]
    df = df.loc[first_date:,:].reset_index(False)
    df = pd.melt(df.iloc[-20:,],id_vars='date',value_name='price')
    if len(assets)%2!=0:
        nrow = ceil(len(assets)/2)
    else:
        nrow = len(assets)
    # Trick to get the asset names into the same grid shape as the page layout
    assets_grid = assets[::]
    # Fill any gap to make the list reshapable by nx3 grid
    assets_grid = assets_grid + abs((2 - nrow)) * [None]
    assets_grid = np.reshape(assets_grid, (nrow, 2))
    temp_child_ls = []
    for i in range(0,nrow):
        if (assets_grid[i,0] is None):
            break
        elif (assets_grid[i,1] is None):
            break
        else:
                titel1 = ' -'.join((assets_grid[i,0],' Change 1D'))
                titel2 = ' -'.join((assets_grid[i,1], ' Change 1D'))
                fig1 = px.line(data_frame=df.loc[df['ticker']==assets_grid[i,0],:],x='date',y='price',title=titel1)
                fig2 = px.line(data_frame=df.loc[df['ticker'] == assets_grid[i,1],:], x='date', y='price',title=titel2)
                row = html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Div([dcc.Graph(figure=fig1)])), \
                                dbc.Col(html.Div([dcc.Graph(figure=fig2)]))
                            ]
                        )
                    ]
                )
                temp_child_ls.append(row)

    new_children = dbc.Container(children=html.Div(temp_child_ls))
    return new_children