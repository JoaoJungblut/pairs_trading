import analysis_manager
import get_fin_data as gfd
import backtest
from pairs_methods import distance_approach as dist
import pandas as pd
import plotly.express as px
import datetime

def main_pipe(ticker_name, start_date, end_date):
    pass


def generate_zscore_fig(ticker_name1, ticker_name2, start_date, end_date = str(datetime.date.today()), pct = 0.7):

    # importing stocks
    stock1 = gfd.get_close_price(ticker_name1, start_date)
    stock2 = gfd.get_close_price(ticker_name2, start_date)

    # spliting in-sample and ou-of-sample
    if pct == None:
        stock1_train, stock1_test = backtest.split_train_test(stock1)
        stock2_train, stock2_test = backtest.split_train_test(stock2)
    else:
        stock1_train, stock1_test = backtest.split_train_test(stock1, pct)
        stock2_train, stock2_test = backtest.split_train_test(stock2, pct)

    # normalizing stocks
    stock1_train_norm, stock1_test_norm = dist.normalize_series(stock1_train, stock1_test)
    stock2_train_norm, stock2_test_norm = dist.normalize_series(stock2_train, stock2_test)

    # calculting spread
    spread_train = dist.spread_distance(stock1_train_norm, stock2_train_norm)
    spread_test = dist.spread_distance(stock1_test_norm, stock2_test_norm)

    # calculating z-score 
    z_score_train = dist.z_score(spread_train, spread_test)
    #z_score_train_test = pd.concat([z_score_train, z_score_test], axis=0).to_frame().reset_index() 
    #z_score_train_test = z_score_train_test.rename(columns={"Adj Close": "Spread"})

    # creating graphic
    fig = px.line(data_frame=z_score_train, x="Date", y= "Spread", title="Z-score of the spread")

    return fig