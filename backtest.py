### Backtest module
### Author: Joao Ramos Jungblut and Matheus Breitenbach
### Last update: 2023-03-08

import pandas as pd
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
        train = x.iloc[:n+1]
        test = x.iloc[n:]
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input must be a pandas.core.frame.DataFrame dtype float64.")
        return -1

    return (train, test)



def position_signal(spread: pd.core.series.Series, open_point: float = 2, close_point: float = 0) -> pd.core.series.Series:
    """
    function to get the open and close signal of operations.

    parameters:
        spread: a pandas Series of pair's spread.
        open_point: the local in spread where you wish to start operation.
        close_point: the local in spread where you wish to end operation.
    """
    
    
    pass


