from dash import Dash, html, Input, Output, dcc
import plotly.express as px
from app import dash_app
import numpy as np
import pandas as pd
from app import universe_ls
from data_dummy import DataDummy
import pdb

data_dummy_obj = DataDummy()


layout = html.Div([html.H1('Crypto Dashboard',className='header',id='page'),\
                  html.Div([dcc.Dropdown(id='dropdown',value='',\
                                         options={ticker:ticker for ticker in universe_ls},multi=True),\
                            html.Br(),\
                            dcc.RadioItems(id='box_plot_type',options=['box', 'violin', 'rug'],\
                                           value='box', inline=True, inputStyle={'margin': '10px'})]),
                  html.Div(children=[dcc.Graph(id='page_content_analytics', figure={})])])

@dash_app.callback(
    Output(component_id='page_content_analytics',component_property='figure'),
    [Input(component_id='dropdown',component_property='value'),\
     Input(component_id='box_plot_type',component_property='value')]
)
def generate_plot(ticker,box_plot_type):
    if ticker != '':
        query = 'SELECT * FROM dummy_data WHERE ticker = "%s" AND indicator = "close"' %ticker
        df = pd.read_sql(sql=query,\
                         con=data_dummy_obj.dummy_conn_obj,index_col='date').drop(['index','indicator','ticker'],axis=1)
        temp_df = df.copy()
        temp_df = temp_df.sort_index()
        temp_df = temp_df.loc[temp_df.index.duplicated('first')]
        temp_df.loc[:,'returns'] = temp_df.loc[:,'price'].pct_change().dropna()
        #title = ' - '.join((ticker,'Return distribution'))
        title = 'Return distribution'
        fig = px.histogram(temp_df,y='returns',marginal=box_plot_type,title =title)
        return fig
    else:
        return {}
