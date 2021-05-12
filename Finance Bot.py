import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
from jupyter_dash import JupyterDash

# Crypto Data - Bitcoin
bitcoin_data = yf.download(tickers='BTC-USD', period='8d', interval='90m')
bitcoin_data = pd.DataFrame(bitcoin_data)
# Moving average using Python Rolling function
bitcoin_data['MA5'] = bitcoin_data['Close'].rolling(5).mean()
bitcoin_data['MA20'] = bitcoin_data['Close'].rolling(20).mean()

# Crypto Data - Ethereum
eth_data = yf.download(tickers='ETH-USD', period='8d', interval='90m')
eth_data = pd.DataFrame(eth_data)
# Moving average using Python Rolling function
eth_data['MA5'] = eth_data['Close'].rolling(5).mean()
eth_data['MA20'] = eth_data['Close'].rolling(20).mean()

# Plotly Figure
fig1 = go.Figure()
fig2 = go.Figure()


app = JupyterDash(__name__)
app.layout = html.Div(children=[
    html.Div([
        html.H1("Bitcoin-USD Data"),
        html.Div(html.P(["Short term MA crosses above the long term MA = buy signal", html.Br(),
                 "Short term MA cross below the long long term MA = sell signal"])),
        dcc.Interval(id='interval-component1',
                     interval=1 * 30000,
                     n_intervals=0
                     ),
        dcc.Graph(id='graph1',
                  figure=fig1),
    ]),
    html.Div([
        html.H1("Ethereum-USD Data"),
        dcc.Interval(id='interval-component2',
                     interval=1 * 30000,  # in milliseconds
                     n_intervals=0
                     ),
        dcc.Graph(id='graph2',
                  figure=fig2),
    ]),
])

# Define callback to update graph
@app.callback(
    Output('graph1', 'figure'),
    [Input('interval-component1', "n_intervals")])
def bitcoin(n):
    # Creating the Graph

    # Candlestick
    x = go.Candlestick(x=bitcoin_data.index, open=bitcoin_data['Open'], high=bitcoin_data['High'], low=bitcoin_data['Low'],
                                 close=bitcoin_data['Close'], name='market data')
    # Add Moving average on the graph
    y = go.Scatter(x=bitcoin_data.index, y=bitcoin_data['MA20'], line=dict(color='blue', width=1.5), name='Long Term MA')
    z = go.Scatter(x=bitcoin_data.index, y=bitcoin_data['MA5'], line=dict(color='orange', width=1.5), name='Short Term MA')

    fig1 = go.Figure(data=[x, y, z])

    # Updating X axis and graph X-Axes
    fig1.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=3, label="3d", step="day", stepmode="backward"),
                dict(count=5, label="5d", step="day", stepmode="todate"),
                dict(step="all")
            ])
        )
    )

    return fig1




# Define callback to update graph
@app.callback(
    Output('graph2', 'figure'),
    [Input('interval-component2', "n_intervals")])
def ethereum(n):
    # Creating the Graph

    # Candlestick
    x = go.Candlestick(x=eth_data.index, open=eth_data['Open'], high=eth_data['High'], low=eth_data['Low'],
                                 close=eth_data['Close'], name='market data')
    # Add Moving average on the graph
    y = go.Scatter(x=eth_data.index, y=eth_data['MA20'], line=dict(color='blue', width=1.5), name='Long Term MA')
    z = go.Scatter(x=eth_data.index, y=eth_data['MA5'], line=dict(color='orange', width=1.5), name='Short Term MA')

    fig2 = go.Figure(data=[x, y, z])

    # Updating X axis and graph X-Axes
    fig2.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=3, label="3d", step="day", stepmode="backward"),
                dict(count=5, label="5d", step="day", stepmode="todate"),
                dict(step="all")
            ])
        )
    )

    return fig2


app.run_server(mode='external', port=8069, dev_tools_ui=True,  # debug=True,
               dev_tools_hot_reload=True, threaded=True, debug=True)

