### Backtest module
### Author: Joao Ramos Jungblut and Matheus Breitenbach
### Last update: 2023-03-08

import pandas as pd
import numpy as np
import warnings


def split_train_test(x: pd.core.series.Series, pct_insample: float = 0.7) -> pd.core.series.Series:
    """
    function to normalize the prices of stocks.
    
    parameters:
        x: a pandas Series.
        pct: a float that specifies the size (percentage) of the in-sample. Default value is equal to 70%. 
    """
    
    try:
        n = round(len(x)*pct_insample)
        train = x.iloc[:n]
        test = x.iloc[n:]
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input must be a pandas.core.frame.DataFrame dtype float64.")
        return -1

    return (train, test)



def generate_signal(Z_score: pd.core.series.Series, open_position: float = 2, close_position: float = 0) -> pd.core.series.Series:
    """
    function to get the open and close signal of operations.

    parameters:
        spread: a pandas Series of pair's spread.
        open_point: the local in spread where you wish to start operation.
        close_point: the local in spread where you wish to end operation.
    """

    try:
        signal = Z_score.copy()
        signal[:] = np.nan

        # we are considering the same threshold for long and short position 
        open_position = np.abs(open_position)
        close_position = np.abs(close_position)

        # initial position
        if Z_score[0] <= -open_position:
            signal[0] = 1
        elif Z_score[0] >= open_position:
            signal[0] = -1
        else:
            signal[0] = 0

        # loop to verify if Z_score crosses threshold long or short
        for t in range(1, len(Z_score)):
            if signal[t-1] == 0:                   # when position is close 
                if Z_score[t] <= -open_position:
                    signal[t] = 1
                elif Z_score[t] >= open_position:
                    signal[t] = -1
                else:
                    signal[t] = 0
            elif signal[t-1] == -1:                # when position is open at threshold long
                if Z_score[t] <= close_position:
                    signal[t] = 0
                else:
                    signal[t] = signal[t-1]
            elif signal[t-1] == 1:                 # when position is open at threshold short
                if Z_score[t] >= -close_position:
                    signal[t] = 0
                else:
                    signal[t] = signal[t-1]
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input must be a pandas.core.frame.DataFrame dtype float64.")
        return -1
    
    return signal



def calculate_stock_return(price_series: pd.core.series.Series) -> pd.core.series.Series:
    """
    This function calculate the return (percentage variation) of stock's price series.
    
    parameters:
        price_series: a pandas Series dtype float64.
    """
    
    try:
        stock_return = np.log(price_series).diff().fillna(0)
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input must be a pandas.core.series.Series dtype float64.")
        return -1
    
    return stock_return



def calculate_trade_return(signal: pd.core.series.Series, x: pd.core.series.Series, y: pd.core.series.Series) -> pd.core.series.Series:
    """
    This function calculate trade's return of the pair.
    
    parameters:
        signal: a pandas Series dtype float64.
        x: a pandas Series dtype float64 and x is the independent variable returns.
        y: a pandas Series dtype float64 and y is the dependent variable returns.
    """
    
    try:
        trade_return = signal.copy()
        trade_return[:] = np.nan
        trade_return[0] = 0                       

        for t in range(1, len(signal)):
            # use t-1 to avoid look-ahead bias
            if signal[t-1] == -1:
                trade_return[t] = np.add(y[t], -x[t])
            if signal[t-1] == 1:
                trade_return[t] = np.add(-y[t], x[t])
            if signal[t-1] == 0:
                trade_return[t] = 0
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input must be a pandas.core.series.Series dtype float64.")
        return -1
    
    return trade_return

