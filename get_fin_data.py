### Module to import and manipulate stock prices
### Author: Joao Ramos Jungblut and Matheus Breitenbach
### Last update: 2023-03-02

import yfinance as yf
import pandas as pd
import datetime
import warnings
import numpy as np


default_end_date = str(datetime.date.today())

def get_close_price(ticker: str, start_date: str, end_date: str = default_end_date) -> pd.core.series.Series:
    """
    function to get the adjusted close price from yfinance package.
    
    parameters:
        ticker: a string with the name of the ticker.
        start_date: a string with the first date of the period.
        end_date: a string with the last date of the period; default option actual day.
    """

    try:
        x = yf.download(ticker, start=start_date, end=end_date)
        x = x.loc[:,"Adj Close"]
    except (TypeError, AttributeError, ValueError):
        warnings.warn("For brazilian stocks you should put '.SA' after ticker name. Example, 'PETR4' should be 'PETR4.SA' ")
        return -1

    return x



def get_intraday_price():
    pass

def export_data():
    pass

def import_data():
    pass



def normalize_serie(x: pd.core.series.Series, pct: float = 0.7) -> pd.core.series.Series:
    """
    function to normalize the prices of stocks.
    
    parameters:
        x: a pandas Series with the price of the stock.
        pct: a float that specifies the size (percentage) of the in-sample. Default value is equal to 70%. 
    """

    try:
        n = round(len(x)*pct)
        in_sample = x.iloc[:n]
        out_sample = x.iloc[n:]

        max_value = np.max(in_sample)
        min_value = np.min(in_sample)
        range_value = max_value - min_value

        normalized_in_sample = in_sample.sub(min_value).div(range_value)
        normalized_out_sample = out_sample.sub(min_value).div(range_value)
        normalized = pd.concat([normalized_in_sample, normalized_out_sample], axis=0)
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input must be a pandas.core.frame.DataFrame dtype float64.")
        return -1

    return normalized



def spread_serie(x: pd.core.series.Series, y: pd.core.series.Series) -> pd.core.series.Series:
    """
    function to calculate the spread betwen two different series.

    parameters:
        x: a pandas Series with the normalized price of stock 1.
        y: a pandas Series with the normalized price of stock 2.
    """

    try:
        difference = x - y
        diff_mean = np.mean(difference)
        diff_std = np.std(difference)
        spread = difference.sub(diff_mean).div(diff_std)
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input x and y must have the same size.")
        warnings.warn("Input must be a pandas.core.series.Series dtype float64.")
        return -1
    
    return spread
