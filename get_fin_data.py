import yfinance as yf
import pandas as pd
import datetime
import warnings
import numpy as np


default_end_date = str(datetime.date.today())
def get_close_price(ticker: str, start_date: str, end_date: str = default_end_date) -> pd.core.frame.DataFrame:
    """
    function to get the adjusted close price from yfinance package.
    
    parameters:
        ticker: a string with the name of the ticker.
        start_date: a string with the first date of the period.
        end_date: a string with the last date of the period; default option actual day.
    """

    df = yf.download(ticker, start=start_date, end=end_date)
    df = df.loc[:,"Adj Close"].to_frame()
    df.rename(columns={"Adj Close": "adj_close"}, inplace=True)


    return df


def normalize_price(stock: pd.core.frame.DataFrame, pct: float) -> pd.core.frame.DataFrame:
    """
    function to normalize the prices of stocks.
    
    parameters:
        stock: a dataframe with the price of the stock.
        pct: a float that specifies the size (percentage) of the in-sample.
    """

    n = round(len(stock)*pct)
    stock_insample = stock.iloc[:n,:]
    stock_outsample = stock.iloc[n:,:]

    price_max = np.max(stock_insample)
    price_min = np.min(stock_insample)
    price_range = price_max - price_min

    norm_price_insample = stock_insample.sub(price_min).div(price_range)
    norm_price_insample.rename(columns={"adj_close": "adj_close_in"}, inplace=True)

    norm_price_outsample = stock_outsample.sub(price_min).div(price_range)
    norm_price_insample.rename(columns={"adj_close": "adj_close_out"}, inplace=True)
    
    norm_price = pd.concat([norm_price_outsample, norm_price_insample], axis=1)

    return norm_price



'''
    if len(stock_one) != len(stock_two):
        warnings.warn("Dataframes with different sizes")
        return -1
'''