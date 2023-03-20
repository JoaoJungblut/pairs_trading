from dash import dash, dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import datetime

import get_fin_data as gfd
from pairs_methods import distance_approach as dist
import backtest


default_end_date = str(datetime.date.today())

def generate_zscore_fig(ticker_name1: str, ticker_name2: str, start_date: str, end_date: str = default_end_date, pct_insample: float = 0.7):

    # importing stocks
    stock1 = gfd.get_close_price(ticker_name1, start_date, end_date)
    stock2 = gfd.get_close_price(ticker_name2, start_date, end_date)

    # spliting in-sample and ou-of-sample
    stock1_train, stock1_test = backtest.split_train_test(stock1)
    stock2_train, stock2_test = backtest.split_train_test(stock2)


    # normalizing stocks
    stock1_train_norm, stock1_test_norm = dist.normalize_series(stock1_train, stock1_test)
    stock2_train_norm, stock2_test_norm = dist.normalize_series(stock2_train, stock2_test)

    # calculting spread
    spread_train = dist.spread_distance(stock1_train_norm, stock2_train_norm)
    spread_test = dist.spread_distance(stock1_test_norm, stock2_test_norm)

    # calculating z-score 
    z_score_train, z_score_test = dist.Z_score(spread_train, spread_test)
    z_score_train_test = pd.concat([z_score_train, z_score_test], axis=0)
    z_score_train_test.rename("Spread", inplace=True)
    z_score_train_test = z_score_train_test.to_frame().reset_index()

    # creating graphic
    fig = px.line(data_frame=z_score_train_test, x="Date", y= "Spread", title=f"{ticker_name1} X {ticker_name2}: Spread")

    return fig



def generate_normalized_fig(ticker_name1: str, ticker_name2: str,start_date: str, end_date: str = default_end_date, pct_insample: float = 0.7):

    stock1 = gfd.get_close_price(ticker_name1, "2021-01-01", "2023-01-01")
    stock_train1, stock_test1 = backtest.split_train_test(stock1)
    stock_train_norm1, stock_test_norm1 = dist.normalize_series(stock_train1, stock_test1)

    stock2 = gfd.get_close_price(ticker_name2, "2021-01-01", "2023-01-01")
    stock_train2, stock_test2 = backtest.split_train_test(stock2)
    stock_train_norm2, stock_test_norm2 = dist.normalize_series(stock_train2, stock_test2)
    
    normalized1  = pd.concat([stock_train_norm1, stock_test_norm1], axis=0)
    normalized1 = normalized1.to_frame().reset_index()
    normalized1 = normalized1.rename(columns={'Adj Close': f'{ticker_name1}'})

    normalized2  = pd.concat([stock_train_norm2, stock_test_norm2], axis=0)
    normalized2 = normalized2.to_frame().reset_index()
    normalized2 = normalized2.rename(columns={'Adj Close': f'{ticker_name2}'})

    normalized = pd.merge(normalized1, normalized2, how='left', on="Date")
    normalized = normalized.set_index("Date")
    fig = px.line(normalized, title=f"{ticker_name1} X {ticker_name2}: Normalized price")
    return fig


zscore_fig = generate_zscore_fig("PETR4.SA", "ITSA4.SA", "2021-01-01")
normalized_price_fig = generate_normalized_fig("PETR4.SA", "ITSA4.SA", "2021-01-01")

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
            dcc.Graph(figure=normalized_price_fig, id='normalized_prices'),
        ])
    ]),
])



# Connecting the Dropdown values to the graph
@app.callback(
    [Output(component_id='zscore_graph', component_property='figure'), 
     Output(component_id='normalized_prices', component_property='figure')],
    [Input(component_id='update_button', component_property='n_clicks')],
    [State(component_id='ticker-1',component_property='value'),
     State(component_id='ticker-2',component_property='value')],
    prevent_initial_call=True
    )
def generate_graph(n, stock1, stock2):
    zscore_fig = generate_zscore_fig(stock1, stock2, "2021-01-01")
    normalized_fig = generate_normalized_fig(stock1, stock2, "2021-01-01")
    return [zscore_fig, normalized_fig]


if __name__ == '__main__':
    app.run_server()#debug=True)