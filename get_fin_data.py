### Module to import, manipulate and export finance data
### Author: Joao Ramos Jungblut and Matheus Breitenbach
### Last update: 2023-03-02

import yfinance as yf
import pandas as pd
import datetime
import warnings



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

def export_data(data: pd.core.series, data_name: str) -> None:
    try:
        import_data
data_name
    except:

        data.to_csv()

def import_dadata(data_name: str: -> pd.DataFrame
    try:
        data = pd.read_csv(f"./data/{data_name}.csv")    paexcept (): #file not found
        warnings.warn("File not found")