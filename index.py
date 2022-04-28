from dash import Dash, html, Input, Output
from pages import home, analytics, bottom_performers, correlation, live_prices, top_performers
import requests
from app import dash_app
from app import server
from app import universe_ls
from data_dummy import DataDummy
import multiprocessing

@dash_app.callback(
    Output(component_id='page-content',component_property='children'),
    Input(component_id='url',component_property='pathname')
)
def display_page(pathname):
    r = requests.get(url=''.join(('http://127.0.0.1:5555',pathname)))
    if r.status_code == 200:
        if pathname == '/':
            return home.layout
        elif pathname == '/pages/analytics.py':
            return analytics.layout
        elif pathname == '/pages/bottom_performers.py':
            return bottom_performers.layout
        elif pathname == '/pages/top_performers.py':
            return top_performers.layout
        elif pathname == '/pages/correlation.py':
            return correlation.layout
        elif pathname == '/pages/live_prices.py':
            return live_prices.layout
        else:
            pass
    else:
        print(html.H2('Error 404: Page not found'))
        return r.status_code
data_dummy_obj = DataDummy()
p1 = multiprocessing.Process(target=data_dummy_obj.live_query,args=[universe_ls])
p2 = multiprocessing.Process(target=dash_app.run_server(debug=True, port=5559))
if __name__ == '__main__':
    test_mutltiprocessing = False
    if test_mutltiprocessing:
        p1.start()
        p2.start()
        p1.join()
        p2.join()
    else:
        dash_app.run_server(debug=True, port=5559)




