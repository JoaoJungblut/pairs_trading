from dash import dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import get_fin_data as gfd
from pairs_methods import distance_approach as dist
import backtest


# pct_change
pct = 0.7

# importing stocks
petr = gfd.get_close_price("PETR4.SA", "2021-01-01")
itsa = gfd.get_close_price("ITSA4.SA", "2021-01-01")

# spliting in-sample and ou-of-sample
petr_train, petr_test = backtest.split_train_test(petr, pct)
itsa_train, itsa_test = backtest.split_train_test(itsa, pct)

# normalizing stocks
petr_train_norm, petr_test_norm = dist.normalize_series(petr_train, petr_test)
itsa_train_norm, itsa_test_norm = dist.normalize_series(itsa_train, itsa_test)

# calculting spread
spread_train = dist.spread_distance(petr_train_norm, itsa_train_norm)
spread_test = dist.spread_distance(petr_test_norm, itsa_test_norm)

# calculating z-score 
z_score_train, z_score_test = dist.z_score(spread_train, spread_test)
z_score_train_test = pd.concat([z_score_train, z_score_test], axis=0).to_frame().reset_index() 
z_score_train_test = z_score_train_test.rename(columns={"Adj Close": "Spread"})

# creating graphic
fig = px.line(data_frame=z_score_train_test, x="Date", y= "Spread", title="Z-score of the spread")


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Stocks"),
        html.Label("Select ticker one", className='dropdown-labels'),
        dcc.Dropdown(multi=True,
                     id='dropdown-1',
                     options=[{'label': "Petrobras", 'value': "PETR4.SA"},
                              {'label': "Itausa", 'value': "ITSA4.SA"},
                              {'label': "Itau", 'value': "ITUB4.SA"},
                              {'label': "Vale", 'value': "VALE3.SA"},
                              {'label': "Ambev", 'value': "ABEV3.SA"},
                              {'label': "Bradesco", 'value': "BBDC4.SA"}]),
        html.Label("Select ticker two", className='dropdown-labels'), 
        dcc.Dropdown(multi=True,
                     id='dropdown-2',
                     options=[{'label': "Petrobras", 'value': "PETR4.SA"},
                              {'label': "Itausa", 'value': "ITSA4.SA"},
                              {'label': "Itau", 'value': "ITUB4.SA"},
                              {'label': "Vale", 'value': "VALE3.SA"},
                              {'label': "Ambev", 'value': "ABEV3.SA"},
                              {'label': "Bradesco", 'value': "BBDC4.SA"}]),
        html.Button("Update"),
        ]),
    html.Div([
        html.Div([
            dcc.Graph(figure=fig),
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)


