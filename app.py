from dash import Dash, html, dcc
from flask import Flask
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from data_dummy import DataDummy



def create_dash_application(flask_app):
    """
    fa fa-icon to be added.
    """
    style_dd = {'color':'#ffffff', 'padding':5}
    px = 23
    dash_app = Dash(server=flask_app, name='Dashboard',url_base_pathname='/',\
                    external_stylesheets=['/static/style/stylesheet.css',\
                                          dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
    dash_app.layout = html.Div( \
        children=\
            [dcc.Location(id='url', refresh=False),\
             html.Div(\
                children=\
                    [html.H2('Overview'),\
                     html.Ul(\
                         children=[html.Li(dcc.Link(children=['home'],href='/pages/home.py',target='_blank')),\
                                   html.Li(dcc.Link(children=['prices'],\
                                                    href='/pages/prices.py',target='_blank')),\
                                   html.Li(dcc.Link(children=['top performers'],\
                                                    href='/pages/top_performers.py',target='_blank')),\
                                   html.Li(dcc.Link(children=['bottom performers'],\
                                                    href='/pages/bottom_performers.py',target='_blank')),\
                                   html.Li(dcc.Link(children=['correlation'],\
                                                    href='/pages/correlation.py',target='_blank')),\
                                   html.Li(dcc.Link(children=['analytics'],\
                                                    href='/pages/analytics.py',target='_blank'))]),\
                     html.Div(children=[html.Div(children=[html.P('Contact', style={'text-align':'center',\
                                                                                    'color':'#ffffff',\
                                                                                    'display':'flex',\
                                                                                    'justify-content':'center'}), \
                     html.Div([html.A(children=DashIconify(icon="fa-brands:twitter",style=style_dd,width=px,height=px),\
                                      href='https://twitter.com/emmanuel_djanga'), \
                               html.A(children=DashIconify(icon="fa-brands:github",style=style_dd,width=px,height=px),\
                                      href='https://github.com/edjanga'), \
                               html.A(children=DashIconify(icon="fa-brands:kaggle",style=style_dd,width=px,height=px),\
                                      href='https://kaggle.com/edjanga'), \
                               html.A(children=DashIconify(icon="fa-brands:github",style=style_dd,width=px,height=px),\
                                      href='https://www.linkedin.com/in/emmanuel-djanga-1b494671'), \
                               html.A(children=DashIconify(icon="fa-at",style=style_dd,width=px,height=px),
                                      href='mailto: emmanuel.djanga@live.be')])])],className='contact',\
                     style={'text-align':'center','position': 'absolute','bottom': 0,'display':'flex',\
                            'justify-content':'center'})],\
                 className='side_nav'),\
                html.Div(children=[],id='page-content',className='main_content')],className='wrapper')

    return dash_app


flask_app = Flask(__name__)
dash_app = create_dash_application(flask_app=flask_app)
server = dash_app.server
universe_ls = ['TSLA', 'TWTR', 'FB', 'MSFT', 'GOOGL', 'AAPL','AMZN','IBM','NFLX','ABNB','ZM']