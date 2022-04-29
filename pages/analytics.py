from dash import Dash, html, Input, Output, dcc
import plotly.express as px
from app import dash_app
import numpy as np
import pandas as pd
from app import universe_ls
from data_dummy import DataDummy
import pdb

data_dummy_obj = DataDummy()

dash_app.title = 'Dashboard | Analytics'
layout = html.Div([html.H1('Crypto Dashboard',className='header',id='page'),\
                  html.Div([html.P('Stock Universe - Select a ticker'),html.Br(),\
                            dcc.Dropdown(id='dropdown',value='',options={ticker:ticker for ticker in universe_ls},\
                                         persistence=True,persistence_type='memory',multi=True),\
                            html.Br(),html.P('Box plot - style'),html.Br(),\
                            dcc.RadioItems(id='box_plot_type',options=['box', 'violin', 'rug'],\
                                           value='box', inline=True, inputStyle={'margin': '10px'})]),
                  html.Div(children=[dcc.Graph(id='page_content_analytics', figure={})])])

#dcc.Interval(id='interval-component',interval=1*1000,n_intervals=0),\

@dash_app.callback(
    Output(component_id='page_content_analytics',component_property='figure'),
    [Input(component_id='dropdown',component_property='value'),\
     Input(component_id='box_plot_type',component_property='value')]
)#,\
#     Input(component_id='interval-component', component_property='n_intervals')
def generate_plot(ticker,box_plot_type):
    if ticker != '':
        if (isinstance(ticker,list))&(len(ticker)>1):
            query = ''
            for index, asset in enumerate(ticker):
                if index == len(ticker) - 1:
                    query = ','.join((query, ''.join((r'"%s"' % asset, ')'))))
                elif index == 0:
                    query = ''.join((query, '(', r'"%s"' % asset))
                else:
                    query = ','.join((query, r'"%s"' % asset))
            query = ' '.join(('SELECT * FROM dummy_data WHERE ticker in', query, 'AND indicator = "close";'))
        else:
            query = 'SELECT * FROM dummy_data WHERE ticker = "%s" AND indicator = "close"' %ticker[0]
        df = pd.read_sql(sql=query,\
                         con=data_dummy_obj.dummy_conn_obj,index_col='date').drop(['index','indicator'],axis=1)
        df = pd.pivot_table(df,values='price',index='date',columns='ticker').pct_change().reset_index(False)
        df.loc[:,'returns'] = df.loc[:,'price'].pct_change()
        df = pd.melt(df,id_vars='date',value_name='returns').dropna()
        filter_s = df['ticker'].isin(ticker)
        title = 'Return distribution'
        fig = px.histogram(df,y='returns',color='ticker',marginal=box_plot_type,title =title)
        return fig
    else:
        return {}