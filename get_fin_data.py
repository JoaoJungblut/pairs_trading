import yfinance as yf
import pandas as pd
import datetime
import warnings
import numpy as np

# exemplo
ticker = "PETR4.SA" 
start_date = "2020-01-01"
end_date = "2022-01-01" 

default= str(datetime.date.today())

def get_close_price(ticker: str, start_date: str, end_date: str = default) -> pd.core.frame.DataFrame:

    """
    function to get the adjusted close price from yfinance package.
    
    parameters:
        ticker: a string with the name of the ticker.
        start_date: a string with the first date of the period.
        end_date: a string with the last date of the period; default option actual day.
    """
    #start_date = datetime.date.today() - datetime.timedelta(years=timespan)
    #end_date = datetime.date.today()
    df = yf.download(ticker, start=start_date, end=end_date)
    df = df.loc[:,"Adj Close"].to_frame()

    return df



test = get_close_price(ticker,start_date, end_date)
print(test)



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
    price_min = np.min(stock_outsample)
    price_range = price_max - price_min
    
    norm_price_insample = stock_insample.sub(price_min).div(price_range)
    norm_price_outsample = stock_outsample.sub(price_min).div(price_range)

    norm_price = pd.concat([norm_price_insample, norm_price_outsample])

    return norm_price

test = normalize_price(test, 0.7)
print(test.tail())

'''
    if len(stock_one) != len(stock_two):
        warnings.warn("Dataframes with different sizes")
        return -1
'''