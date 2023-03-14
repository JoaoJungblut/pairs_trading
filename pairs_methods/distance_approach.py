### Distance approach module
### Author: Joao Ramos Jungblut and Matheus Breitenbach
### Last update: 2023-03-08

import numpy as np
import pandas as pd
import warnings


def normalize_series(x_train: pd.core.series.Series, x_test: pd.core.series.Series = None) -> pd.core.series.Series:
    """
    function to normalize the prices of stocks.

    parameters:
        x_train: a pandas Series with the price of the stock.
        x_test: a pandas Series with the price of the stock.
    """

    try:
        max_train = np.max(x_train)
        min_train = np.min(x_train)

        normalized_train = x_train.sub(min_train).div(max_train - min_train)

        if x_test is not None:
            normalized_test = x_test.sub(min_train).div(max_train - min_train)
            return normalized_train, normalized_test
        else:
            return normalized_train

    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input must be a pandas.core.frame.DataFrame dtype float64.")
        return -1



def spread_distance(x: pd.core.series.Series, y: pd.core.series.Series) -> pd.core.series.Series:
    """
    function to calculate the spread betwen two different series.

    parameters:
        x: a pandas Series with the normalized price of independent stock.
        y: a pandas Series with the normalized price of dependent stock.
    """

    try:
        spread = np.subtract(y, x)
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input x and y must have the same size.")
        warnings.warn("Input must be a pandas.core.series.Series dtype float64.")
        return -1
    
    return spread



def Z_score(spread_train: pd.core.series.Series, spread_test: pd.core.series.Series) -> pd.core.series.Series:
    """
    function to get the Z-score of the spread.

    parameters:
        x_train: a pandas Series with the price of the stock.
        x_test: a pandas Series with the price of the stock.
    """

    try:
        mean_train = np.mean(spread_train)
        std_train = np.std(spread_test)

        z_score_train = spread_train.sub(mean_train).div(std_train)

        if spread_test is not None:
            z_score_test = spread_test.sub(mean_train).div(std_train)
            return (z_score_train, z_score_test)
        else:
            return z_score_train

    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input must be a pandas.core.frame.DataFrame dtype float64.")
        return -1



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

