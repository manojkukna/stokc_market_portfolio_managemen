
# import os
#
# try:
#     import xlwings
# except ImportError:
#     os.system('python -m pip install --upgrade pip')
#
# try:
#     import xlwings
# except ImportError:
#     os.system('python -m pip install xlwings==0.30.12')
# try:
#     import pandas
# except ImportError:
#     os.system('python -m pip install pandas')
#
#
# try:
#     import yfinance
# except ImportError:
#     os.system('python -m pip install yfinance==0.2.28')
# try:
#     import tabulate
# except ImportError:
#     os.system('python -m pip install tabulate')
#
#
# try:
#     import pyotp
# except ImportError:
#     os.system('python -m pip install pyotp')





import xlwings
import pandas as pd
import math
import yfinance as yf
# from datetime import datetime, timedelta
import datetime
import time
import traceback
import copy
from tabulate import tabulate
# import datetime, time
# from datetime import datetime
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


import xlwings
Book_NAME = "data_NSC_ALL2.xlsx"


import pyotp
from kite_trade import *


def time_():
    time_ = time.strftime("%H:%M:%S", time.localtime())
    return (time_)


def exl_sheets_clear(sheets_name):
    ws = xlwings.Book(Book_NAME).sheets(sheets_name)
    ws.clear()


def exl_sheets_list(exl_sheets_list):
    for i in exl_sheets_list:
        exl_sheets_clear(sheets_name=i)


def tickers_add_BO_NS(tickers, EXCHANGE):
    count = 0
    for tickers_list1 in tickers:
        tickers[count] = str(f"{tickers_list1}.{EXCHANGE}")
        count = count + 1
    return tickers


def nsc_bse_index(index, NSC_BSC_index):
    data = pd.read_csv("NIFTY 50.csv")
    if NSC_BSC_index == 0:
        NSC_BSC_index = None
    data = list(data[index][:NSC_BSC_index].values)
    remove_nan_None = [x for x in data if
                       x is not None and not (isinstance(x, float) and math.isnan(x))]
    return remove_nan_None


def print_sheets(df, sheets_name, range):
    ws = xlwings.Book(Book_NAME).sheets(sheets_name)
    ws.range(range).value = pd.DataFrame(df.round(2))


def yfinance_download(tickers_list, start_date, end_date,interval):
    yfinance_download = yf.download(tickers_list, start_date, end_date, interval=interval)['Adj Close']
    yfinance_download = yfinance_download.fillna(method='ffill', axis=0)
    yfinance_download = yfinance_download.fillna(method='bfill')


    # print(yfinance_download)
    yfinance_download.index.name = 'Date'
    df = pd.to_datetime(yfinance_download.index)
    yfinance_download['Date'] = df
    yfinance_download.set_index('Date', inplace=True)
    yfinance_download.index = yfinance_download.index.strftime('%d-%m-%Y- %H:%M:%S')
    print_sheets(df=yfinance_download, sheets_name="Adj Close", range="A1")
    return yfinance_download


def yfinance_download_high(yfinance_download_high):
    yfinance_download_high = yfinance_download_high.cummax()
    yfinance_download_high = yfinance_download_high.shift(1).fillna(method='bfill')
    print_sheets(df=yfinance_download_high, sheets_name="HIGH", range="A1")
    print("def yfinance_download_high 130 ",time_())
    return yfinance_download_high


def opne_time_data(list,start_date,end_date,interval):
    dataindex = yf.download(list, start_date, end_date, interval=interval)['Adj Close']

    df_filled_column = dataindex.fillna(method='ffill', axis=0)
    df_filled_column.index.name = 'Date'
    fast_data_row = df_filled_column.head(1)
    print("def opne_time_data 143 ",time_())
    return fast_data_row


def real_time_data(list,start_date):
    dataindex = yf.download(list, start_date, None, interval="1m")['Adj Close']
    df_filled_column = dataindex.fillna(method='ffill', axis=0)
    df_filled_column.index.name = 'Date'
    last_data = df_filled_column.tail(1)
    print("def real_time_data 152 ",time_())
    time.sleep(1)
    return last_data

def read_csv_df(csv_lokesan):
    read_csv_df1 = pd.DataFrame(pd.read_csv(str(csv_lokesan), on_bad_lines='skip'))
    csv_lokesan = pd.read_csv(csv_lokesan)
    read_csv_df = read_csv_df1.loc[:, ~csv_lokesan.columns.str.contains('^Unnamed')]
    print("read_csv_d 160 ", time_())
    return read_csv_df


def live_market_df(DATE,yfinance_download_transpose,yfinance_download_high_transpose,strategy):
    live_market = pd.DataFrame()
    DATE = DATE
    index = yfinance_download_transpose.columns.get_loc(DATE)
    live_market["DATE"] = DATE
    live_market = pd.DataFrame(live_market["DATE"])

    live_market["opne"] = yfinance_download_transpose.iloc[:, 0]
    live_market["Close"] = yfinance_download_transpose.iloc[:, index]
    live_market["high"] = yfinance_download_high_transpose.iloc[:, index]
    live_market["PARSENT"] = (yfinance_download_transpose.iloc[:,index] - yfinance_download_transpose.
                              iloc[:,0]) / yfinance_download_transpose.iloc[:,0] * 100



    live_market["PARSENT_high%"] = (yfinance_download_high_transpose.iloc[:,index] - yfinance_download_high_transpose.iloc[:,
                                    0]) / yfinance_download_high_transpose.iloc[:, 0] * 100
    live_market["CHANGE"] = yfinance_download_transpose.iloc[:, index] - yfinance_download_transpose.iloc[:, 0]
    live_market["Rank_PARSENT"] = live_market["PARSENT"].rank(ascending=0)
    live_market["Rank_high"] = live_market["PARSENT_high%"].rank(ascending=0)
    live_market["DATE"] = DATE

    live_market.index.name = 'symbol'

    if strategy == "Rank_high":
        live_market.sort_values("Rank_high", axis=0, ascending=True, inplace=True)
    else:
        live_market.sort_values("Rank_PARSENT", axis=0, ascending=True, inplace=True)


    return live_market







def intraday_market_df(opne_time_data,real_time_data,strategy,yfinance_download_high):
    opne_time_data = pd.DataFrame(opne_time_data)
    pd_apend_data2 = opne_time_data.append(real_time_data)
    pd_apend_data = pd_apend_data2.transpose()



    csv_lokesan ='z_download_high_appd.csv'

    read_csv_df1 = pd.DataFrame(pd.read_csv(str(csv_lokesan), on_bad_lines='skip'))
    csv_lokesan = pd.read_csv(csv_lokesan)
    read_csv_df = read_csv_df1.loc[:, ~csv_lokesan.columns.str.contains('^Unnamed')]
    # print("read_csv_d 173 ", time_())






    print_sheets(df= pd_apend_data2, sheets_name="Adj Close", range="A1")

    download_high_df1 = read_csv_df1.append(real_time_data)

    download_high_df = download_high_df1.cummax()

    # print(pd_apend_data2)
    # print( download_high_df)

    Entry_csv_appd = pd.DataFrame(download_high_df).to_csv(
        'z_download_high_appd.csv', mode='w', index=False, header=True)
    print_sheets(df= download_high_df, sheets_name="HIGH", range="A1")


    # print(  download_high_df)

    # breakpoint()
    download_high_appd = download_high_df.transpose()
    intraday_market = pd.DataFrame()
    intraday_market["DATE"] = pd_apend_data.columns[-1]
    intraday_market = pd.DataFrame(intraday_market["DATE"])
    intraday_market["opne"] = pd_apend_data.iloc[:, 0]
    intraday_market["Close"] = pd_apend_data.iloc[:, -1]
    intraday_market["high"] = download_high_appd.iloc[:, -2]
    intraday_market["CHANGE"] = intraday_market["Close"] - intraday_market["opne"]
    intraday_market["PARSENT"] =intraday_market["CHANGE"] / intraday_market["opne"] * 100

    intraday_market["PARSENT_high%"] =(intraday_market["high"] - intraday_market["opne"]) /  intraday_market["opne"]  *100
    intraday_market["Rank_PARSENT"] = intraday_market["PARSENT"].rank(ascending=0)
    intraday_market["Rank_high"] = intraday_market["PARSENT_high%"].rank(ascending=0)
    intraday_market["DATE"] = pd_apend_data.columns[-1]

    intraday_market.index.name = 'symbol'
    if strategy == "Rank_high":
        intraday_market.sort_values("Rank_high", axis=0, ascending=True, inplace=True)
    else:
        intraday_market.sort_values("Rank_PARSENT", axis=0, ascending=True, inplace=True)
    return intraday_market





live_market_dict = {"symbol": None, "DATE": None, "opne": None, "Close": None, "high": None,
         "PARSENT": None, "PARSENT_high%": None,"CHANGE": None, "Rank_PARSENT": None,"Rank_high":None,
         "RANIG_STOCK": None,}
buy_dict = {"symbol": None, "strategy": None, "Buy": None, "Entry": None, "avg": None, "Close": None, "high": None,"low":None,
         "stoplos": None, "Entry Date": None,"capital": None, "quantity": None,"PNL":None, "invested": None,
            "current": None, "Fees": None,"T1": None, "T2": None, "T3": None, "T4": None, "T5": None, "circuit": None,}
sell_dict = {"symbol": None, "strategy": None, "Buy": None, "Entry": None, "avg": None, "Close": None, "high": None,
         "stoplos": None, "Entry Date": None,
         "capital": None, "quantity": None,"PNL":None, "invested": None, "current": None, "Fees": None,
         "T1": None, "T2": None, "T3": None, "T4": None, "T5": None, "circuit": None,}
holdings_dict = {"Entry Date": None, "symbol": None, "strategy": None, "Buy": None, "Entry": None, "avg": None,
          "Close": None, "high": None,"low":None, "stoplos": None, "quantity": 0, "invested": None,
          "current": None, "capital": None, "Fees": None, "PNL": None, "% PNL": None,
          "T1": None, "T2": None, "T3": None, "T4": None, "T5": None, "circuit": None, }





#
# sheets_list = ["NSE", "holdings", "orders", "Adj Close", "Volume",
#                "HIGH", "upper_circuit_count"]
# exl_sheets_list(exl_sheets_list=sheets_list)
#
# nsc_bse_index = nsc_bse_index(index="NIFTY 200", NSC_BSC_index=0)         # BSE SHOCK LIST LIG
#         # https: // www.bseindia.com / corporates / List_Scrips.html
#
# symbol_list = tickers_add_BO_NS(tickers=nsc_bse_index,
#                                 EXCHANGE="NS")  # + tickers_add_BO_NS(tickers=data11, EXCHANGE="BO")
#
#
#
# # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
#
#
#

# madi
# FromDay = "01"  # FromDay = "22"
# FromMonth = "11"  # FromMonth = "11"
# FromYear = "2024"  # FromYear = "2022"
# interval = "1d"
# index_dasy = 0
# count_DATE = 0
# start_date = f'{FromYear}-{FromMonth}-{FromDay}'
#
#
#
# if index_dasy == 0:
#     index_dasy = None
#
#                # madi
# tomDay = "21"  # FromDay = "20"
# toMonth = "02"  # FromMonth = "03"
# toYear = "2024"  # FromYear = "2023"
# #
# end_date2 = f'{toYear}-{toMonth}-{tomDay}'
#
#
# end_date = end_date2
# end_date = None
#
#
# strategy = "Rank_PARSENT"     #  "Rank_high"  "Rank_PARSENT"
#
# capital = 5000.00
# Close_limit_max = capital
# Close_limit_mimi = 5

# yfinance_download = yfinance_download(tickers_list=symbol_list, start_date=start_date, end_date=end_date,interval=interval)
# yfinance_download_high = yfinance_download_high(yfinance_download_high=yfinance_download)
# yfinance_download_transpose = yfinance_download.transpose()
# yfinance_download_high_transpose = yfinance_download_high.transpose()
# DATE_list = pd.DataFrame(yfinance_download.index)

# print(yfinance_download.round(2))
#
# live_market_data = live_market_df(DATE=DATE_list["Date"][count_DATE])
#
# live_market = live_market_data.loc[live_market_data['Close'] > Close_limit_mimi]
# if not Close_limit_max == 0:
#     live_market = live_market_data.loc[live_market_data['Close'] < Close_limit_max]
#
# print(live_market)