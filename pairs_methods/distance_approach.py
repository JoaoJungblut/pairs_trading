### Distance approach module
### Author: Joao Ramos Jungblut and Matheus Breitenbach
### Last update: 2023-03-08

import numpy as np
import pandas as pd
import warnings


def normalize_train(x_train: pd.core.series.Series) -> pd.core.series.Series:
    """
    function to normalize the prices of stocks at in_sample data.
    
    parameters:
        x_train: a pandas Series with the price of the stock.
    """

    try:
        max_train = np.max(x_train)
        min_train = np.min(x_train)

        normalized = x_train.sub(min_train).div(max_train-min_train)
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input must be a pandas.core.frame.DataFrame dtype float64.")
        return -1

    return normalized


def normalize_test(x_train: pd.core.series.Series, x_test: pd.core.series.Series) -> pd.core.series.Series:
    """
    function to normalize the prices of stocks at out_of_sample data.
    
    parameters:
        x_train: a pandas Series with the price of the stock.
        x_test: a pandas Series with the price of the stock.
    """

    try:
        max_train = np.max(x_train)
        min_train = np.min(x_train)

        normalized = x_test.sub(min_train).div(max_train-min_train)
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input must be a pandas.core.frame.DataFrame dtype float64.")
        return -1

    return normalized


def spread_distance(x: pd.core.series.Series, y: pd.core.series.Series) -> pd.core.series.Series:
    """
    function to calculate the spread betwen two different series.

    parameters:
        x: a pandas Series with the normalized price of stock 1.
        y: a pandas Series with the normalized price of stock 2.
    """

    try:
        spread = np.subtract(x, y)
    except (TypeError, AttributeError, ValueError):
        warnings.warn("Input x and y must have the same size.")
        warnings.warn("Input must be a pandas.core.series.Series dtype float64.")
        return -1
    
    return spread


def z_score():
    pass




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

