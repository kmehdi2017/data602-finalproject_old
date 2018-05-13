import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
#from pandas_datareader import data as web
from datetime import datetime
from gdax import GDAX

app = dash.Dash()

app.layout = html.Div([
    html.H1('Crypocurrency Tickers'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'ETH-USD', 'value': 'ETH-USD'},
            {'label': 'BTC-USD', 'value': 'BTC-USD'},
            {'label': 'BCH-USD', 'value': 'BCH-USD'},
            {'label': 'XRP-USD', 'value': 'XRP-USD'},
            {'label': 'LTC-USD', 'value': 'LTC-USD'}
        ],
        value='COKE'
    ),
    dcc.Graph(
        id='my-graph' #,
       # figure = {
        #    'layout': {
         #       'title': 'Crypocurrency Ticker Historical Price Chart '
          #  }
        #}        
    )
])

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
#def update_graph(selected_dropdown_value):
    #df = web.DataReader(
    #    selected_dropdown_value, data_source='google',
    #    start=dt(2017, 1, 1), end=dt.now())
    #return {
    #    'data': [{
    #        'x': df.index,
    #        'y': df.Close
    #    }]
    #}

def update_graph(selected_dropdown_value):
    df = GDAX(selected_dropdown_value).fetch(datetime(2017, 10, 1), datetime.now(), 1440)
    df.index = df.index.astype('int').astype("datetime64[s]")
    return {
        'data': [{
            'x': df.index,
            'y': df.close
        }]
    }

if __name__ == '__main__':
    app.run_server( debug=True, host='0.0.0.0')
