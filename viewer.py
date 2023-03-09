from dash import Dash, dcc, html, Input, Output
import matplotlib.pyplot as plt
import get_fin_data as gfd
from pairs_methods import distance_approach as dist


petr = gfd.get_close_price("PETR4.SA", "2021-01-01")
itsa = gfd.get_close_price("ITSA4.SA", "2021-01-01")

x_normalized = dist.normalize_serie(petr)
y_normalized = dist.normalize_serie(itsa)
spread = dist.distance_spread(x_normalized, y_normalized)

fig, ax = plt.subplots()
ax.plot(x_normalized.index, x_normalized, color="blue")
ax.plot(spread.index, spread, color="pink")
ax.plot(y_normalized.index, y_normalized, color="red")
ax.axhline(1)
ax.axhline(0)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(['"PETR4.SA"', 'ITSA4.SA', 'ITUB4.SA', "VALE3.SA", "ABEV3.SA", "BBDC4"], 'BBDC4', id='dropdown'),
    html.Div(id='dd-output-container'),
    dcc.Dropdown(['"PETR4.SA"', 'ITSA4.SA', 'ITUB4.SA', "VALE3.SA", "ABEV3.SA", "BBDC4"], 'BBDC4', id='dropdown'),
    html.Div(id='dd-output-container'),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'


#if __name__ == '__main__':
app.run_server(debug=True)

