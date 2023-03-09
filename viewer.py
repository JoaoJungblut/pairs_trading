from dash import Dash, dcc, html, Input, Output
import matplotlib.pyplot as plt
import pandas as pd
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
spread_train = dist.spread_distance(petr_train_norm, petr_train_norm)
spread_test = dist.spread_distance(itsa_test_norm, itsa_test_norm)

# calculating z-score 
z_score_train, z_score_test = dist.z_score(spread_train, spread_test)
z_score_train_test = pd.concat([z_score_train, z_score_test], axis=0)

# creating graphic
fig, ax = plt.subplots()
ax.plot(z_score_train_test, color="black")
ax.axhline(0, color="red", linestyle="dashed")
ax.axhline(2, color="green", linestyle="dashed")
ax.axhline(-2, color="green", linestyle="dashed")
ax.axvline(len(z_score_train), color="yellow", linestyle="dotted")



app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(options=[{'label': "PETR4.SA", 'value': "PETR4.SA"},
                           {'label': "ITSA4.SA", 'value': "ITSA4.SA"},
                           {'label': "ITUB4.SA", 'value': "ITUB4.SA"},
                           {'label': "VALE3.SA", 'value': "VALE3.SA"},
                           {'label': "ABEV3.SA", 'value': "ABEV3.SA"},
                           {'label': "BBDC4", 'value': "BBDC4"}], 
                 value='BBDC4', 
                 id='dropdown'),
    html.Div(id='dd-output-container'),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


@app.callback(
    Output('dd-output-container', 'children'),
    Input('dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'


app.run_server(debug=True)


