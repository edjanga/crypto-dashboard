from dash import Dash, html, Input, Output, dcc
import plotly.express as px
from app import dash_app
import numpy as np
import pandas as pd
from app import universe_ls
from data_dummy import DataDummy

data_dummy_obj = DataDummy()


layout = html.Div([html.H1('Crypto Dashboard',className='header',id='page'),\
                  html.Div([html.P('Stock Universe - Select a ticker'),html.Br(),dcc.Dropdown(id='dropdown',value='',\
                                         options={ticker:ticker for ticker in universe_ls}),\
                            html.Br(),html.P('Box plot - style'),html.Br(),\
                            dcc.RadioItems(id='box_plot_type',options=['box', 'violin', 'rug'],\
                                           value='box', inline=True, inputStyle={'margin': '10px'})]),
                  html.Div(children=[dcc.Interval(id='interval-component',interval=1*1000,n_intervals=0),\
                                     dcc.Graph(id='page_content_analytics', figure={})])])

@dash_app.callback(
    Output(component_id='page_content_analytics',component_property='figure'),
    [Input(component_id='dropdown',component_property='value'),\
     Input(component_id='box_plot_type',component_property='value'),\
     Input(component_id='interval-component', component_property='n_intervals')]
)
def generate_plot(ticker,box_plot_type,n):
    if ticker != '':
        if isinstance(ticker,list):
            ticker = ticker[0]
        query = 'SELECT * FROM dummy_data WHERE ticker = "%s" AND indicator = "close"' %ticker
        df = pd.read_sql(sql=query,\
                         con=data_dummy_obj.dummy_conn_obj,index_col='date').drop(['index','indicator','ticker'],axis=1)
        df.loc[:,'returns'] = df.loc[:,'price'].pct_change()
        df = df.dropna()
        title = 'Return distribution'
        fig = px.histogram(df,y='returns',marginal=box_plot_type,title =title)
        return fig
    else:
        return {}