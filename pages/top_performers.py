from dash import Dash, html, Input, Output, dcc
import plotly.express as px
from app import dash_app
import numpy as np


layout = html.Div([html.H1('Crypto Dashboard',className='header',id='page')])
