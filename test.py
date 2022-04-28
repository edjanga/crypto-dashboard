from dash import Dash, html
import dash_bootstrap_components as dbc

external_stylesheets = [
    {"href":"/static/style/stylesheet.css"},\
    {"href":"https://kit.fontawesome.com/fe68b6d84f.js"},
]

app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([

    html.Div([
           html.I(className="fa-solid fa-house-chimney"),
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=True, port=3333)