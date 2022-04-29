from dash import Dash, html, Input, Output, dcc
import dash_bootstrap_components as dbc
from app import dash_app
import plotly.express as px
from data_dummy import DataDummy
from app import dash_app
import pandas as pd
from math import ceil
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
    nrow = ceil(len(assets)%3)
    count = 0
    temp_child_ls = []
    while count <= nrow:
        for num in range(0,len(assets)-2):
            if num%3==0:
                temp_child_ls.append(\
                    dbc.Row(\
                        children=[\
                            dbc.Col(\
                                children=\
                                    dbc.Card(\
                                        children=\
                                            [dbc.CardBody(\
                                                children=[dbc.Row(children=[dbc.Col(children=[assets[num],\
                                                                                              html.P('Change 1D')])]),\
                                                          dbc.Row(children=[dbc.Col(children=[])])])]))]))
                temp_child_ls.append( \
                    dbc.Row( \
                        children=[ \
                            dbc.Col( \
                                children= \
                                    dbc.Card( \
                                        children= \
                                            [dbc.CardBody( \
                                                children=[dbc.Row(children=[dbc.Col(children=[assets[num+1], \
                                                                                              html.P('Change 1D')])]), \
                                                          dbc.Row(children=[dbc.Col(children=[])])])]))]))
                temp_child_ls.append( \
                    dbc.Row( \
                        children=[ \
                            dbc.Col( \
                                children= \
                                    dbc.Card( \
                                        children= \
                                            [dbc.CardBody( \
                                                children=[dbc.Row(children=[dbc.Col(children=[assets[num+2], \
                                                                                              html.P('Change 1D')])]), \
                                                          dbc.Row(children=[dbc.Col(children=[])])])]))]))
        count += 1
                #temp_child_ls.append(dbc.Row(children=[]))
                #temp_child_ls.append(dbc.Row(children=[]))
                        # # Asset #2
                        #     dbc.Col( \
                        #         dbc.Card( \
                        #             [dbc.CardBody( \
                        #                 dbc.Row( \
                        #                     [dbc.Col([assets[num+1]]), dbc.Col([html.P('Daily change')])]), \
                        #                 dbc.Row(dbc.Col([])))])), \
                        #     # Asset #3
                        #     dbc.Col( \
                        #         dbc.Card( \
                        #             [dbc.CardBody( \
                        #                 dbc.Row( \
                        #                     [dbc.Col([assets[num]]), dbc.Col([html.P('Daily change')])]), \
                        #                 dbc.Row(dbc.Col([])))]))]))
                #container_all_cards_ls.append(temp_child_ls)
    new_children = dbc.Container(children=temp_child_ls)
    return new_children