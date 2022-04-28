"""
This is the script for getting all kinds of information on equities from multiple sources. 
Date of creation: Apr 12 2022
version: 0.1
"""
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from datetime import date
import threading
import time
import yfinance as yf
import pandas as pd
import warnings
import os

#ask for command line input
if __name__ == "__main__":
    stock_ticker = input("please provide a ticker symbol: ")
    if stock_ticker is not None and not file_stock_exist_or_not(stock_ticker):
        wrangle_stock(stock_ticker)



#function to check if the data was already downloaded or whether it is still needed to download from yfinance.
def file_stock_exist_or_not(ticker_symbol):
    directory_path = os.getcwd()
    if os.path.isfile(directory_path+"/stocks_fundamentals/{}_curated_fundamentals.csv".format(ticker_symbol)):
        print("Already existing file for {} found".format(ticker_symbol))
        return True
    else:
        print("no existing stock data found for {} - Downloading...".format(ticker_symbol))
        return False


def wrangle_stock(ticker_symbol):
    
    stock_object = yf.Ticker(ticker_symbol)
    
    #copying the yfinance object so we have a dataframe from witch we can drop the "Net Income" column that appears in both financials and cashflow.
    stock_cashflow = stock_object.cashflow.copy()
    stock_cashflow = stock_cashflow.drop(index= "Net Income")

    stock_financials = stock_object.financials.copy()
    
    fundamentals_stock = pd.concat([stock_cashflow, stock_financials], sort = True)

    # .T flips the columns and rows, so it flips the axis if you will.
    fundamentals_stock = fundamentals_stock.T
    fundamentals_stock = fundamentals_stock.fillna(0)
    fundamentals_stock.index.rename("Date", inplace = True)
    
    # get the last 5 years of given stock prices. 
    stock_prices = stock_object.history(period = "5y")
    stock_prices = stock_prices.drop(columns = ["Open", "High", "Low", "Dividends", "Stock Splits"])
    # In order to filter out the warning about the future deprecation of get_lock()
    warnings.filterwarnings("ignore")
    
    # getting the 4 time stamps for when the fundamentals were published.
    time_1, time_2,time_3,time_4 = fundamentals_stock.index[0], fundamentals_stock.index[1], fundamentals_stock.index[2],fundamentals_stock.index[3]

    #this gets the indexes of the closest dates in stock_prices to the dates we have from fundamentals_stock, which should be 4. 
    relevant_dates_index = [stock_prices.index.get_loc(time_1, method = "nearest"),stock_prices.index.get_loc(time_2, method = "nearest"),stock_prices.index.get_loc(time_3, method = "nearest"),stock_prices.index.get_loc(time_4, method = "nearest")]

    #Creating a dictionary that matches the time stamps we got from fundamentals_stock to the nearest time stamps we will find from the stock_prices, so that we can replace the former with the later for the price info in order to merge the 2.
    time_relations_dict = {}
    for each in range(len(fundamentals_stock)):
        time_relations_dict[stock_prices.iloc[stock_prices.index.get_loc(fundamentals_stock.index[each], method = "nearest")].name] = fundamentals_stock.index[each]


    stock_prices = stock_prices.iloc[relevant_dates_index]

    for each in range(len(stock_prices)):
        stock_prices.rename(index={stock_prices.index[each]: time_relations_dict[stock_prices.index[each]]}, inplace = True)

    complete_stock_dataframe = pd.concat([fundamentals_stock, stock_prices], axis = 1)

    #getting all the column names of the df.
    features = []
    for col in complete_stock_dataframe.columns:
        features.append(col)
    # only 2 since we only get 4 years worth of data from yfinance
    lags = 2
    #storing the names of the new columns, not currently used in script.
    cols = []
    
    #creating lags for each column.
    for f in features:
        for lag in range(1, lags + 1):
            col = "{}_lag_{}".format(f, lag)
            complete_stock_dataframe[col] = complete_stock_dataframe[f].shift(lag)
            cols.append(col)
    # droping the rows that do not have lag data as there is no older data. will leave only 2 rows with current data as data is only 4 years old, to improve in the future will need another data source that goes further back.

    complete_stock_dataframe["FutureDirection"] = complete_stock_dataframe["Close"].shift(periods = -1) / complete_stock_dataframe["Close"]
    complete_stock_dataframe.dropna(inplace = True)

    #get the current day to add to the name of the file to make sure if in the future more up to date data is needed for a stock.
    today = date.today()
    #complete_stock_dataframe.to_csv("stocks_fundamentals/{}_fun_{}.csv".format(ticker_symbol, today))
    return complete_stock_dataframe




