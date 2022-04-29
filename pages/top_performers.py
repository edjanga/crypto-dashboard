from dash import Dash, html, Input, Output, dcc
import plotly.express as px
from app import dash_app
from app import universe_ls
from data_dummy import DataDummy
import pandas as pd
import pdb

dash_app.title = 'Dashboard | Top Performers'
layout = html.Div([html.H1('Crypto Dashboard',className='header',id='page'),\
                   html.Br(),\
                   html.Div(children=[],id='page_content_top_performers')])



@dash_app.callback(
    Output(component_id='page_content_top_performers',component_property='children'),
    Input(component_id='url',component_property='pathname')
)
def filter_heatmap(pathname):
    data_dummy_obj = DataDummy()
    assets = pd.read_sql('SELECT DISTINCT ticker FROM dummy_data;',con=data_dummy_obj.dummy_conn_obj)
    assets = assets.ticker.tolist()
    assets.sort()
    query = ''
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
    df = df.pct_change().dropna().sort_index()
    top_performers_ls = df.iloc[-1,:].sort_values(ascending=False).index[:3].tolist()
    df = df[top_performers_ls].round(3)
    fig = px.bar(data_frame=df.iloc[-1,:],text_auto=True,title='Top Performers',labels={'value':'returns',\
                                                                                           'variable':''})
    new_children = [html.Br(),dcc.Graph(id='top_performers',figure=fig)]
    return new_children
