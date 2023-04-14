### controller module, with the main pipe
### Author: Joao Ramos Jungblut and Matheus Breitenbach
### Last update: 2023-04-13

from dash import dash, dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px

import get_fin_data as gfd
from pairs_methods import distance_approach as dist
import backtest
import viewer
import ticket_list


def main_pipe(ticker_name1: str, ticker_name2: str, start_date: str):
    """
    
    """

    # importing stocks
    stock1 = gfd.get_close_price(ticker_name1, start_date)
    stock2 = gfd.get_close_price(ticker_name2, start_date)

    # spliting train and test base
    stock1_train, stock1_test = backtest.split_train_test(stock1)
    stock2_train, stock2_test = backtest.split_train_test(stock2)

    # normalizing stocks
    stock1_train_norm, stock1_test_norm = dist.normalize_series(stock1_train, stock1_test)
    stock2_train_norm, stock2_test_norm = dist.normalize_series(stock2_train, stock2_test)
    stock1_train_test_norm = pd.concat([stock1_train_norm, stock1_test_norm], axis=0)
    stock2_train_test_norm = pd.concat([stock2_train_norm, stock2_test_norm], axis=0)

    # calculating spread
    spread_train = dist.spread_distance(stock1_train_norm, stock2_train_norm)
    spread_test = dist.spread_distance(stock1_test_norm, stock2_test_norm)

    # calculating z-score
    z_score_train, z_score_test = dist.Z_score(spread_train, spread_test)
    z_score_train_test = pd.concat([z_score_train, z_score_test], axis=0)

    # generating signal
    signal = backtest.generate_signal(z_score_train_test, 1, 0)

    # calculate stock returns
    stock1_rtn = backtest.calculate_stock_return(stock1)
    stock2_rtn = backtest.calculate_stock_return(stock2)

    # calculate trade return
    trade_return = backtest.calculate_trade_return(signal, stock1_rtn, stock2_rtn)
    cum_trade_return = backtest.calculate_compound_return(trade_return)

    # generating graphs
    zscore_fig = viewer.generate_zscore_fig(z_score_train_test, signal, ticker_name1, ticker_name2)
    normalized_price_fig = viewer.generate_normalized_fig(stock1_train_test_norm, stock2_train_test_norm, ticker_name1, ticker_name2)
    trade_return_fig = viewer.generate_trade_returns_fig(cum_trade_return)
    
    return zscore_fig, normalized_price_fig, trade_return_fig


zscore_fig, normalized_price_fig, trade_return_fig = main_pipe("PETR4.SA", "ITSA4.SA", "2021-01-01")


app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.Div([
        html.H1("Stocks"),
        html.Label("Select ticker one", className='dropdown-labels'),
        dcc.Dropdown(multi=False,
                     id='ticker-1',
                     options=ticket_list.TICKETS,
                              value='PETR4.SA'),
        html.Label("Select ticker two", className='dropdown-labels'), 
        dcc.Dropdown(multi=False,
                     id='ticker-2',
                     options=ticket_list.TICKETS,
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
            dcc.Graph(figure=normalized_price_fig, id='normalized_prices_graph'),
        ])
    ]),
    html.Div([
        html.Div([
            dcc.Graph(figure=trade_return_fig, id='return_graph'),
        ])
    ]),
])


@app.callback(
    [Output(component_id='zscore_graph', component_property='figure'), 
     Output(component_id='normalized_prices_graph', component_property='figure'),
     Output(component_id='return_graph', component_property='figure')],
    [Input(component_id='update_button', component_property='n_clicks')],
    [State(component_id='ticker-1',component_property='value'),
     State(component_id='ticker-2',component_property='value')],
    prevent_initial_call=True
    )
def generate_graph(n, stock1, stock2):
    zscore_fig, normalized_price_fig, trade_return_fig = main_pipe(stock1, stock2, "2021-01-01")
    return [zscore_fig, normalized_price_fig, trade_return_fig]