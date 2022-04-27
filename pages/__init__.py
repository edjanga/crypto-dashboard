from dash import Dash, html

PORT = 8051
def create_dash_application(flask_app):
    dash_app = Dash(server=flask_app, name='Dashboard',url_base_pathname='/',\
                    external_stylesheets=['/static/style/stylesheet.css'])
    dash_app.layout = html.Div(html.Div(html.Div(html.H1(children='Hello World'),className="main_content")),\
                               className='wrapper')
    dash_app.run_server(debug=True, port=PORT)
    html.Div()