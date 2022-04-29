from dash import html, Input, Output, dcc
import plotly.express as px
from app import dash_app
from data_dummy import DataDummy
import pandas as pd
import pdb

dash_app.title = 'Dashboard | Correlation'
layout = html.Div([html.H1('Crypto Dashboard',className='header',id='page'),\
                   html.Br(),\
                   html.Div(id='assets_checklist'),\
                   html.Div(children=[],id='page_content_correlation')])


@dash_app.callback(
    Output(component_id='assets_checklist',component_property='children'),
    Input(component_id='url',component_property='pathname')
)
def asset_check_list(pathname):
    data_dummy_obj = DataDummy()
    assets = pd.read_sql('SELECT DISTINCT ticker FROM dummy_data;',con=data_dummy_obj.dummy_conn_obj)
    assets = assets.ticker.tolist()
    assets.sort()
    return [dcc.Checklist(id='assets',options={asset:asset for asset in assets},value=assets,\
                                 inputStyle={'margin': '10px'},persistence=True,persistence_type='memory')]

@dash_app.callback(
    Output(component_id='page_content_correlation',component_property='children'),
    Input(component_id='assets',component_property='value')
)
def update_plot(ticker_ls):
    data_dummy_obj = DataDummy()
    assets = pd.read_sql('SELECT DISTINCT ticker FROM dummy_data;', con=data_dummy_obj.dummy_conn_obj)
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
    df = df.loc[:,df.columns.isin(ticker_ls)]
    df = df.pct_change().dropna()
    df = df.corr().round(2).sort_index()
    fig = px.imshow(df[ticker_ls],text_auto=True, aspect='auto',\
                    title='Correlation of returns',color_continuous_scale='agsunset')
    new_children = [html.Br(),\
                    dcc.Graph(id='heatmap',figure=fig)]
    return new_children
