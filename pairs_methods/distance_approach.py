### Distance approach module
### Author: Joao Ramos Jungblut and Matheus Breitenbach
### Last update: 2023-03-07

import numpy as np
import pandas as pd
import warnings

# corrigir função
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


# corrigir função
def distance_spread(x: pd.core.series.Series, y: pd.core.series.Series) -> pd.core.series.Series:
    """
    function to calculate the spread betwen two different series.

    parameters:
        x: a pandas Series with the normalized price of stock 1.
        y: a pandas Series with the normalized price of stock 2.
    """

    try:
        difference = np.subtract(x, y)
        diff_mean = np.mean(difference)
        diff_std = np.std(difference)
        spread = difference.sub(diff_mean).div(diff_std)
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input x and y must have the same size.")
        warnings.warn("Input must be a pandas.core.series.Series dtype float64.")
        return -1
    
    return spread



def calculate_euclidean_distance(x: pd.core.series.Series, y: pd.core.series.Series) -> float: 
    """
    function to calculate the euclidean distance between two pandas Series.

    parameters:
        x: a pandas Series with the normalized price of stock 1.
        y: a pandas Series with the normalized price of stock 2.
    """

    try:
        euclidean_distance = np.sqrt(np.sum(np.square(np.subtract(x, y))))
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input x and y must have the same size.")
        warnings.warn("Input must be a pandas.core.series.Series dtype float64.")
        return -1

    return euclidean_distance



def calculate_correlation(x: pd.core.series.Series, y: pd.core.series.Series) -> float:
    """
    function to calculate the correlation between two pandas Series.

    parameters:
        x: a pandas Series with the normalized price of stock 1.
        y: a pandas Series with the normalized price of stock 2.
    """

    try:
        correlation = np.corrcoef(x, y)
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input x and y must have the same size.")
        warnings.warn("Input must be a pandas.core.series.Series dtype float64.")
        return -1

    return correlation[1, 0]

