from __future__ import division



import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from flask import Flask

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True #avoid warning

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
        
        html.Div([html.Img(src='https://www.potnetwork.com/sites/default/files/uploads/article/3804/these-three-pot-stocks-will-help-cannabis-stock-bubble-burst.jpeg',
             width="400", height="300")],
                    style={'textAlign': 'center'}),
    html.H1(children="Financial Risk Management System", style={'textAlign': 'center',}),
    html.H3(children="Authors: Yifan Wu, Yiding Xie, Qianfeng Ying", style={'textAlign': 'center',}),
    html.H6(children="The calculation system has the capability of taking a portfolio with any given stocks or options.",
                    style={'textAlign': 'center'}),
    html.H6(children="Please click on bottoms below to enter the calculation system.",
                    style={'textAlign': 'center'}),
    html.Br(),
    html.Div([dcc.Link('Individual Stock Only', href='/page-1')],style={'textAlign': 'center'}),
    html.Br(),
    html.Div([dcc.Link('Portfolio Only', href='/page-2')],style={'textAlign': 'center'}),
    html.Br(),
    html.Div([dcc.Link('Portfolio With Option', href='/page-3')],style={'textAlign': 'center'}),
])

app_1_layout = html.Div([
    # dcc.Tabs(id="tabs", value='tab-1', children=[
    #     dcc.Tab(label='Tab one', value='tab-1',children=[
         html.Div([
                html.H3(children='Individual Stock', style={
                    'textAlign': 'center',
                }),
                html.Div([
                    html.Label('Ticker:'),
                    dcc.Input(id='ticker', type='text', value='XOM'),

                    html.Label('Initial Investments:'),
                    dcc.Input(id='invest', type='text', value='10000'),

                    html.Label('Window (years):'),
                    dcc.Input(id='window', type='text', value='5'),

                    html.Label('Position:'),
                    dcc.Dropdown(id='position',
                                 options=[
                                     {'label': 'Long', 'value': 'long'},
                                     {'label': 'Short', 'value': 'short'}
                                 ],
                                 value='long'
                                 ,style={'width': '70%'}),
                ],
                    style={'width': '30%', 'display': 'inline-block'}),

                html.Div([
                    html.Label('Start date:'),
                    dcc.Input(id="start", type='date', value='1998-01-01'),

                    html.Label('VaR Percentage:'),
                    dcc.Input(id="var", type='text', value='0.99'),

                    html.Label('Horizon (days):'),
                    dcc.Input(id='horizon', type='text', value='5'),
                ],
                    style={'width': '30%', 'display': 'inline-block'}),

                html.Div([
                    html.Label('End Date'),
                    dcc.Input(id='end', type='date', value='2018-12-01'),

                    html.Label('ES Percentage:'),
                    dcc.Input(id='es', type='text', value='0.975'),

                    html.Label('Risk Method:'),
                    dcc.Dropdown(id='method',
                                 options=[
                                     {'label': 'Parametric VaR/ES', 'value': 'Parametric'},
                                     {'label': 'Histroical VaR/ES', 'value': 'Historical'},
                                     {'label': 'Monte Carlo VaR/ES', 'value': 'Monte Carlo'}
                                 ],
                                 value='Parametric'
                                 ),
                ],
                    style={'width': '30%', 'display': 'inline-block','vertical-align': 'text-bottom'}),

                html.Div([
                    html.Label("Output:"),
                    dcc.Dropdown(id="output",
                                 options=[
                                     {'label': 'Price Plot', 'value': 'price'},
                                     {'label': 'Risk Plot', 'value': 'risk'},
                                     {'label': 'Backtesting Plot', 'value': "backtest"}
                                 ],
                                 value='price'
                                 ),
                    html.Button(id='submit', n_clicks=0, children='Submit'),
                ], style={'textAlign': 'center'}),

                # html.Div([
                #     dcc.Graph(id='indicator-graphic')
                # ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'})

                dcc.Graph(id='indicator-graphic-1'),]),
                
    html.Div([dcc.Link('Portfolio Only', href='/page-2')],style={'textAlign': 'center'}),
    html.Br(),
    html.Div([dcc.Link('Portfolio With Option', href='/page-3')],style={'textAlign': 'center'}),
    html.Br(),
    html.Div([dcc.Link('Go back to home', href='/')],style={'textAlign': 'center'}),
                ])


@app.callback(
    Output('indicator-graphic-1', 'figure'),
    [Input('submit', 'n_clicks')],
    [State("output","value"),
     State('ticker', 'value'),
     State('invest', 'value'),
     State('start', 'value'),
     State('end', 'value'),
     State("position","value")
     #State('input-5-state', 'value'),
     #State('input-6-state', 'value'),
     #State('input-7-state', 'value'),
     #State('input-8-state', 'value')
     ])

def update_graph(nclicks,output,stock, invest, start, end,position):
    if (nclicks > 0):
        if (output == "price"):
            if (position == "long"):
                pos= float(1)
            else: pos = float(-1)
            pricedata = web.DataReader(stock, 'yahoo', start, end)['Adj Close'].sort_index(ascending=True)
            pricedata = pd.DataFrame(pricedata)#.reset_index()
            pricedata.columns = ["Price"]
            invest = float(invest)*pos
            amount = (invest/pricedata.iat[0, 0])
            pricedata["Price"] = pricedata["Price"] * amount

            return {
                'data': [go.Scatter(
                x=pricedata.index,
                y=pricedata['Price'],
                #text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
                mode='lines+markers',
                marker={
                    'size': 1,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )],
                'layout': go.Layout(
                    xaxis={
                        'title': "Date",
                    },
                    yaxis={
                        'title': "Stock Price",
                    },
                    margin={'l': 40, 'b': 40, 't': 40, 'r': 0},
                    hovermode='closest'
                )
            }


app_2_layout = html.Div([
         html.Div([
                html.H3(children='Portfolio', style={
                    'textAlign': 'center',
                }),
                html.H6(
                    children='For the price and risk plots of portfolio, enter the parameter below.You need to split stocks by comma.',
                    style={
                        'textAlign': 'center'
                    }
                ),
                html.Div([
                    html.Label('Ticker:'),
                    dcc.Input(id='ticker', type='text', value='AAPL,XOM,CSCO'),
                    html.Label('Initial Investments:'),
                    dcc.Input(id='invest', type='text', value='10000'),

                    html.Label('Window (years):'),
                    dcc.Input(id='window', type='text', value='5'),
                    html.Label("Weights:"),
                    dcc.Input(id='weights', type='text', value='0.1,0.2,0.7'),
                ],
                    style={'width': '30%', 'display': 'inline-block'}),

                html.Div([
                    html.Label('Start date:'),
                    dcc.Input(id="start", type='date', value='1998-01-01'),

                    html.Label('VaR Percentage:'),
                    dcc.Input(id="var", type='text', value='0.99'),

                    html.Label('Horizon (days):'),
                    dcc.Input(id='horizon', type='text', value='5'),
                ],
                    style={'width': '30%', 'display': 'inline-block'}),

                html.Div([
                    html.Label('End Date'),
                    dcc.Input(id='end', type='date', value='2018-01-01'),

                    html.Label('ES Percentage:'),
                    dcc.Input(id='es', type='text', value='0.975'),

                    html.Label('Risk Method:'),
                    dcc.Dropdown(id='method',
                                 options=[
                                     {'label': 'Parametric VaR/ES', 'value': 'Parametric'},
                                     {'label': 'Histroical VaR/ES', 'value': 'Historical'},
                                     {'label': 'Monte Carlo VaR/ES', 'value': 'Monte Carlo'}
                                 ],
                                 value='Parametric'
                                 ),
                ],
                    style={'width': '30%', 'display': 'inline-block','vertical-align': 'text-bottom'}),
                html.Br(),
                html.Div([
                    html.Label("Output:"),
                    dcc.Dropdown(id="output",
                                 options=[
                                     {'label': 'Price Plot', 'value': 'price'},
                                     {'label': 'Risk Plot', 'value': 'risk'},
                                     {'label': 'Backtesting Plot', 'value': "backtest"}
                                 ],
                                 value='price'
                                 )]),
                html.Br(),
                html.Div([
                    html.Button(id='submit', n_clicks=0, children='Submit'),
                ], style={'textAlign': 'center'}),

                # html.Div([
                #     dcc.Graph(id='indicator-graphic')
                # ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'})
                dcc.Graph(id='indicator-graphic-2'),
                #html.Div(id='indicator-graphic-2'),
                
    html.Br(),
    html.Div([dcc.Link('Individual Stock Only', href='/page-1')],style={'textAlign': 'center'}),
    html.Br(),
    html.Div([dcc.Link('Portfolio With Option', href='/page-3')],style={'textAlign': 'center'}),
    html.Br(),
    html.Div([dcc.Link('Go back to home', href='/')],style={'textAlign': 'center'}),            
                
                ]),


                ])
@app.callback(
    #Output('indicator-graphic-2', 'children'),
    Output('indicator-graphic-2', 'figure'),
    [Input('submit', 'n_clicks')],
    [State("output","value"),
     State('ticker', 'value'),
     State('start', 'value'),
     State('end', 'value'),
     State('invest', 'value'),
     State('weights', 'value'),
     #State('input-5-state', 'value'),
     #State('input-6-state', 'value'),
     #State('input-7-state', 'value'),
     #State('input-8-state', 'value')
     ])

def update_graph2(nclicks,output,stock, start, end,invest,weights):
    if (nclicks > 0):
        if (output == "price"):
            weight = weights.split(",")
            weight = list(map(float,weight))
            #return u"{}{} {}".format(float(weight[0]),float(weight[1]),float(weight[2]))
            stock =stock.split(",")
            pricedata = web.DataReader(stock, 'yahoo', start, end)['Adj Close'].sort_index(ascending=True)
            pricedata = pd.DataFrame(pricedata)#.reset_index()
            #pricedata.columns = ["Price"]
            invest = float(invest)
            amount = np.array(weight)*invest
            priceall = amount*pricedata
            priceall= priceall.sum(axis=1)

            return {
                'data': [
                    go.Scatter(
                    x=pricedata.index,
                    y=priceall,
                    #text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
                    mode='lines+markers',
                    marker={
                        'size': 1,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    }

            )
                ],
                'layout': go.Layout(
                    xaxis={
                        'title': "Date",
                    },
                    yaxis={
                        'title': "Stock Price",
                    },
                    margin={'l': 30, 'b': 40, 't': 40, 'r': 0},
                    hovermode='closest'
                )
            }


app_3_layout = html.Div([
         html.Div([
                html.H3(children='Portfolio with Option', style={
                    'textAlign': 'center',
                }),
                html.H6(
                    children='This page can calculate VaR that can be reduced by liquidating a portion of a single stock portfolio to hedge with put options.',
                    style={
                        'textAlign': 'center'
                    }
                ),
                html.Div([
                    html.Label('Ticker:'),
                    dcc.Input(id='ticker', type='text', value='AAPL,XOM,CSCO'),
                    html.Label('Initial Investments:'),
                    dcc.Input(id='invest', type='text', value='10000'),

                    html.Label('Window (years):'),
                    dcc.Input(id='window', type='text', value='5'),
                ],
                    style={'width': '30%', 'display': 'inline-block'}),

                html.Div([
                    html.Label('Start date:'),
                    dcc.Input(id="start", type='date', value='1998-01-01'),

                    html.Label('VaR Percentage:'),
                    dcc.Input(id="var", type='text', value='0.99'),

                    html.Label('Horizon (days):'),
                    dcc.Input(id='horizon', type='text', value='5'),
                ],
                    style={'width': '30%', 'display': 'inline-block'}),

                html.Div([
                    html.Label('End Date'),
                    dcc.Input(id='end', type='date', value='2018-01-01'),
                    html.Br(),
                    html.Label('Risk Method:'),
                    dcc.Dropdown(id='method',
                                 options=[
                                     {'label': 'Parametric VaR', 'value': 'Parametric'},
                                     {'label': 'Histroical VaR', 'value': 'Historical'},
                                     {'label': 'Monte Carlo VaR', 'value': 'Monte Carlo'}
                                 ],
                                 value='Parametric'
                                 ),
                ],
                    style={'width': '30%','display': 'inline-block','vertical-align': 'text-bottom'}),

                html.Div([
                    html.Label("Output:"),
                    dcc.Dropdown(id="output",
                                 options=[
                                     {'label': 'Price Plot', 'value': 'price'},
                                     {'label': 'Risk Plot', 'value': 'risk'},
                                     {'label': 'Backtesting Plot', 'value': "backtest"}
                                 ],
                                 value='price'
                                 )]),
                html.Br(),
                html.Div([
                    html.Button(id='submit', n_clicks=0, children='Submit'),
                ], style={'textAlign': 'center'}),

                # html.Div([
                #     dcc.Graph(id='indicator-graphic')
                # ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'})

                dcc.Graph(id='indicator-graphic-3'),
                
    html.Br(),
    html.Div([dcc.Link('Individual Stock Only', href='/page-1')],style={'textAlign': 'center'}),
    html.Br(),
    html.Div([dcc.Link('Portfolio Only', href='/page-2')],style={'textAlign': 'center'}),
    html.Br(),
    html.Div([dcc.Link('Go back to home', href='/')],style={'textAlign': 'center'}),
                
                ])])



@app.callback(
    Output('indicator-graphic-3', 'figure'),
    [Input('submit', 'n_clicks')],
    [State("output","value"),
     State('ticker', 'value'),
     State('invest', 'value'),
     State('start', 'value'),
     State('end', 'value')
     #State('input-5-state', 'value'),
     #State('input-6-state', 'value'),
     #State('input-7-state', 'value'),
     #State('input-8-state', 'value')
     ])

def update_graph3(nclicks,output,stock, invest, start, end):
    if (nclicks > 0):
        if (output == "price"):
            pricedata = web.DataReader(stock, 'yahoo', start, end)['Adj Close'].sort_index(ascending=True)
            pricedata = pd.DataFrame(pricedata)#.reset_index()
            pricedata.columns = ["Price"]
            invest = float(invest)
            amount = (invest/pricedata.iat[0, 0])
            pricedata["Price"] = pricedata["Price"] * amount

            return {
                'data': [go.Scatter(
                x=pricedata.index,
                y=pricedata.iloc[:,0],
                name=pricedata.columns[0],
                #text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
                mode='lines+markers',
                marker={
                    'size': 1,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }

            )
                ],


                'layout': go.Layout(
                    xaxis={
                        'title': "Date",
                    },
                    yaxis={
                        'title': "Stock Price",
                    },
                    margin={'l': 40, 'b': 40, 't': 40, 'r': 0},
                    hovermode='closest'
                )
            }

@app.callback(
    Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return app_1_layout
    elif pathname == '/page-2':
        return app_2_layout
    elif pathname == '/page-3':
        return app_3_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)

