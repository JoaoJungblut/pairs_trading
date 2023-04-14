### Viewer module
### Author: Joao Ramos Jungblut and Matheus Breitenbach
### Last update: 2023-03-08

import pandas as pd
import plotly.express as px


def generate_zscore_fig(z_score: pd.core.series.Series, signal: pd.core.series.Series, ticker_name1: str, ticker_name2: str):
    """
    
    """

    z_score = z_score.rename("Spread", inplace=True)
    z_score = z_score.to_frame().reset_index()
    signal = signal.rename("Signal", inplace=True)
    signal = signal.to_frame().reset_index()

    df_zscore_signal = pd.merge(z_score, signal, how='left', on="Date")
    df_zscore_signal = df_zscore_signal.set_index("Date")

    fig = px.line(df_zscore_signal, title=f"{ticker_name1} X {ticker_name2}: Spread")

    return fig


def generate_normalized_fig(stock1_norm: pd.core.series.Series, stock2_norm: pd.core.series.Series, ticker_name1: str, ticker_name2: str):
    """
    
    """

    stock1_norm = stock1_norm.to_frame().reset_index()
    stock1_norm = stock1_norm.rename(columns={'Adj Close': f'{ticker_name1}'})

    stock2_norm = stock2_norm.to_frame().reset_index()
    stock2_norm = stock2_norm.rename(columns={'Adj Close': f'{ticker_name2}'})

    df_norm = pd.merge(stock1_norm, stock2_norm, how='left', on="Date")
    df_norm = df_norm.set_index("Date")

    fig = px.line(df_norm, title=f"{ticker_name1} X {ticker_name2}: Normalized price")

    return fig


def generate_trade_returns_fig(cum_trade_return: pd.core.series.Series):
    """
    
    """

    cum_trade_return = cum_trade_return.rename("Cumulative Return", inplace=True)
    cum_trade_return = cum_trade_return.to_frame().reset_index()
    cum_trade_return = cum_trade_return.set_index("Date")

    fig = px.line(cum_trade_return, title=f"Profit")

    return fig

