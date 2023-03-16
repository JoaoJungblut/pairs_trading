from dash import dash, dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import get_fin_data as gfd
from pairs_methods import distance_approach as dist
import backtest
import controller



zscore_fig = controller.generate_zscore_fig("PETR4.SA", "ITSA4.SA", "2021-01-01")
ticker1_normalized_fig = controller.generate_normalized_fig("PETR4.SA", "2021-01-01")
ticker2_normalized_fig = controller.generate_normalized_fig("ITSA4.SA", "2021-01-01")

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.Div([
        html.H1("Stocks"),
        html.Label("Select ticker one", className='dropdown-labels'),
        dcc.Dropdown(multi=False,
                     id='ticker-1',
                     options=[{'label': "Petrobras", 'value': "PETR4.SA"},
                              {'label': "Itausa", 'value': "ITSA4.SA"},
                              {'label': "Itau", 'value': "ITUB4.SA"},
                              {'label': "Vale", 'value': "VALE3.SA"},
                              {'label': "Ambev", 'value': "ABEV3.SA"},
                              {'label': "Bradesco", 'value': "BBDC4.SA"}],
                              value='PETR4.SA'),
        html.Label("Select ticker two", className='dropdown-labels'), 
        dcc.Dropdown(multi=False,
                     id='ticker-2',
                     options=[{'label': "Petrobras", 'value': "PETR4.SA"},
                              {'label': "Itausa", 'value': "ITSA4.SA"},
                              {'label': "Itau", 'value': "ITUB4.SA"},
                              {'label': "Vale", 'value': "VALE3.SA"},
                              {'label': "Ambev", 'value': "ABEV3.SA"},
                              {'label': "Bradesco", 'value': "BBDC4.SA"}],
                              value="ITSA4.SA"),
        html.Button("Update", id="update_button"),
        ]),
    html.Div([
        html.Div([
            dcc.Graph(figure=zscore_fig, id='zscore_graph'),
        ])
    ]),
    html.Div([
        html.Div([
            dcc.Graph(figure=ticker1_normalized_fig, id='normalized_ticker1'),
        ])
    ]),
    html.Div([
        html.Div([
            dcc.Graph(figure=ticker2_normalized_fig, id='normalized_ticker2'),
        ])
    ])
])



# Connecting the Dropdown values to the graph
@app.callback(
    [Output(component_id='zscore_graph', component_property='figure'), 
     Output(component_id='normalized_ticker1', component_property='figure'), 
     Output(component_id='normalized_ticker2', component_property='figure')],
    [Input(component_id='update_button', component_property='n_clicks')],
    [State(component_id='ticker-1',component_property='value'),
     State(component_id='ticker-2',component_property='value')],
    prevent_initial_call=True
    )
def generate_graph(n, stock1, stock2):
    zscore_fig = controller.generate_zscore_fig(stock1, stock2, "2021-01-01")
    ticker1_normalized_fig = controller.generate_normalized_fig(stock1, "2021-01-01")
    ticker2_normalized_fig = controller.generate_normalized_fig(stock2, "2021-01-01")
    return [zscore_fig, ticker1_normalized_fig, ticker2_normalized_fig]


if __name__ == '__main__':
    app.run_server()#debug=True)