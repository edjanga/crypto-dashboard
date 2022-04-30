from dash import html, dcc

layout = html.Div([html.H1(children=[html.B('Tech Stock Dashboard')],className='header',id='page'),\
                   html.Div([html.H2('Welcome on my Tech Stock Dashboard',style={'text-align':'center'}),\
                             html.Br(),\
                             html.P(\
                    children=[html.B('This dashboard tracks and provides analytics for a set of tech stocks.')]),\
                             html.Br(),\
                             html.Ul(children=[html.Li([html.B('Prices'),' - Latent prices fetched from ',\
                                                                 dcc.Link(href='https://www.alphavantage.co/'),\
                                                                 ],style={'marginBottom':15}),\
                                               html.Li([html.B('Top Performers'),' - Top 3 performer stocks'],\
                                                       style={'marginBottom':15}), \
                                               html.Li([html.B('Bottom Performers'), ' - Bottom 3 performer stocks'], \
                                                       style={'marginBottom': 15}), \
                                               html.Li([html.B('Correlation'),\
                                                        ' - Heatmap of stock returns of all stocks in the universe'], \
                                                       style={'marginBottom': 15}),\
                                               html.Li([html.B('Analytics'), \
                                                        ' - Distribution and Boxplot of stock returns.'], \
                                                       style={'marginBottom': 15})])],style={'font-size':25}, )])
