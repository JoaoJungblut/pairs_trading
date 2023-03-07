### Backtest module
### Author: Joao Ramos Jungblut and Matheus Breitenbach
### Last update: 2023-03-07

import pandas as pd
import warnings


def position_signal(spread: pd.core.series.Series, open_point: float = 2, close_point: float = 0) -> pd.core.series.Series:
    """
    function to get the open and close signal of operations.

    parameters:
        spread: a pandas Series of pair's spread.
        open_point: the local in spread where you wish to start operation.
        close_point: the local in spread where you wish to end operation.
    """
    pass
