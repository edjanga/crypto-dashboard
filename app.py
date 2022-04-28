from dash import Dash, html, dcc
from flask import Flask
from data_dummy import DataDummy



def create_dash_application(flask_app):
    """
    fa fa-icon to be added.
    """
    dash_app = Dash(server=flask_app, name='Dashboard',url_base_pathname='/',\
                    external_stylesheets=['/static/style/stylesheet.css'],suppress_callback_exceptions=True)
    dash_app.layout = html.Div( \
        children=\
            [dcc.Location(id='url', refresh=False),\
             html.Div(\
                children=\
                    [html.H2('Overview'),\
                     html.Ul(\
                         children=[html.Li(dcc.Link(children=['home'],href='/pages/home.py')),\
                                   html.Li(dcc.Link(children=['live prices'],href='/pages/live_prices.py')),\
                                   html.Li(dcc.Link(children=['top performers'],href='/pages/top_performers.py')),\
                                   html.Li(dcc.Link(children=['bottom performers'],href='/pages/bottom_performers.py')),\
                                   html.Li(dcc.Link(children=['correlation'],href='/pages/correlation.py')),\
                                   html.Li(dcc.Link(children=['analytics'],href='/pages/analytics.py'))]),\
                     html.Div(children=[html.P('Contact')],className='contact')],className='side_nav'), \
                html.Div(children=[],id='page-content',className='main_content')],className='wrapper')

    return dash_app

flask_app = Flask(__name__)
dash_app = create_dash_application(flask_app=flask_app)
server = dash_app.server
universe_ls = ['TSLA', 'TWTR', 'FB', 'MSFT', 'GOOGL', 'AAPL']