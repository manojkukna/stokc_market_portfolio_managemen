import yfinance as yf
import pandas as pd
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
import data_prossig as dp
import copy




# import data_prossig as dp
import copy



# Define the date range   Balance
start_date = "2020-03-01"
end_date = "2025-03-31"
interval = "1d"       # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
Balance = 2000
start_price_limit = 1000
stock_nabar = 50
index = "NIFTY MIDSMALLCAP 400"
percentage_high = 20



# NIFTY 20	NIFTY 50	NIFTY NEXT 50	NIFTY 200	NIFTY MIDCAP 50	  NIFTY MIDCAP 100	NIFTY MIDSMALLCAP 400   NSC ALL   	NIFTY TOTAL MARKET	NIFTY 200 cv	NSC ALL	BSE ALL








sheets_list = ["NSE", "holdings", "orders", "Adj Close", "Volume",
               "HIGH", "upper_circuit_count"]
dp.exl_sheets_list(exl_sheets_list=sheets_list)



#       24   3854.41
#      23      1229.35    1130.91          7587.53    2028.54           1935.29                17801.49                  89078.61
# NIFTY 20	NIFTY 50	NIFTY NEXT 50	NIFTY 200	NIFTY MIDCAP 50	  NIFTY MIDCAP 100	NIFTY MIDSMALLCAP 400   NSC ALL   	NIFTY TOTAL MARKET	NIFTY 200 cv	NSC ALL	BSE ALL




nsc_bse_index = dp.nsc_bse_index(index=index , NSC_BSC_index=stock_nabar)         # BSE SHOCK LIST LIG
        # https: // www.bseindia.com / corporates / List_Scrips.html

# print(len(nsc_bse_index),nsc_bse_index)
#
#


symbol_list = dp.tickers_add_BO_NS(tickers=nsc_bse_index,EXCHANGE="NS")  # + tickers_add_BO_NS(tickers=data11, EXCHANGE="BO")

# print("symbol_list 1",symbol_list)
#

# breakpoint()





# Define the list of 20 NSE tickers
nse_tickers = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "HDFC.NS",
    "ICICIBANK.NS", "KOTAKBANK.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS",
    "LT.NS", "HINDUNILVR.NS", "ASIANPAINT.NS", "MARUTI.NS", "AXISBANK.NS",
    "BAJFINANCE.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "DMART.NS", "ULTRACEMCO.NS"
]






results = []




# start_price_limit


yfinance_download =dp.yfinance_download(tickers_list=symbol_list, start_date=start_date, end_date=end_date,interval=interval).round(2)

# NaN कॉलम हटाएं
df_cleaned =yfinance_download.dropna(axis=1, how='all')



yfinance_download = df_cleaned
# print("Cleaned DataFrame:")
# print(df_cleaned)


# 0th इंडेक्स पर 500 से कम वाली कॉलम्स को फिल्टर करें
filtered_columns = [col for col in yfinance_download.columns if col == "Date" or (yfinance_download [col].iloc[0] < start_price_limit if pd.notna(yfinance_download [col].iloc[0]) else False)]

df_filtered = yfinance_download[filtered_columns]
#
# print("Filtered DataFrame:")
# print(df_filtered)


yfinance_download = df_filtered
print(yfinance_download)

#
# breakpoint()






symbol_list = yfinance_download.columns


# breakpoint()


# yfinance_download=yfinance_download.loc[(yfinance_download < start_price_limit)]



# print(yfinance_download)
# #
# #
#
# breakpoint()
cunt =len(nse_tickers)


entry_list_Holding = []


# percentage= 10
# new_value = (value * percentage / 100)




def stock_invesh(stock_df, ticker, index, column, percentage):



    if index > 0:
        # stock_df_lave = pd.DataFrame(entry_list_Holding).round(2)


        # breakpoint()

        new_value = (stock_df.iloc[index, column] * percentage / 100)
        # print(ticker, "shisft",stock_df.iloc[index -1, column].round(2), "ltp", stock_df.iloc[index, column].round(2))

        columns = ["Ticker", "start_date", "start_price", "end_date", "end_price","high", "Change", "Percentage",
                   "Percentage_HIGH","Rank_PARSENT", "invested"]

        results_last =pd.DataFrame(results, columns=columns)


        df_results_last= results_last.loc[(results_last['Ticker'] == ticker) ]
        # print(df_results_last)
        # breakpoint()

        df_results_last =  df_results_last.drop_duplicates(subset=['Ticker'], keep='last')

        # print(df_results_last)
        #
        # print("column",df_results_last.columns.get_loc("Percentage"))
        #
        # print("shisft",df_results_last.iloc[0, df_results_last.columns.get_loc("high")])
        # results_current = pd.DataFrame(results, columns=columns)
        results_current = pd.DataFrame(stock_df)
        results_current.reset_index()
        # print(results_current.head(10))

        # print("current", results_current.iloc[index,  results_current.columns.get_loc(ticker)])

        new_value = (df_results_last.iloc[0, df_results_last.columns.get_loc("high")]  * percentage / 100)



        if df_results_last.iloc[0, df_results_last.columns.get_loc("high")]  <  results_current.iloc[index,  results_current.columns.get_loc(ticker)] - new_value:
            invesh = Balance / 2
            qtt_ = int( invesh  / df_results_last.iloc[0, df_results_last.columns.get_loc("end_price")] )
            invesh = df_results_last.iloc[0, df_results_last.columns.get_loc("end_price")]  *   qtt_

            # print("high","index", index, "column", ticker,
            #       "shisft", df_results_last.iloc[0, df_results_last.columns.get_loc("high")],
            #       "current", results_current.iloc[index, results_current.columns.get_loc(ticker)],
            #          "invesh" ,invesh                      )
            #

        else:

              invesh = 0.00

              # print("low", "index", index, "column", ticker,
              #       "shisft", df_results_last.iloc[0, df_results_last.columns.get_loc("high")],
              #       "current", results_current.iloc[index, results_current.columns.get_loc(ticker)],
              #       "high", invesh)


        return invesh



    if index == 0:
         results_current = pd.DataFrame(stock_df)
         results_current.reset_index()
         # invesh = Balance





         qtt_ = int(float(Balance) / results_current.iloc[index, results_current.columns.get_loc(ticker)])
         invesh = results_current.iloc[index, results_current.columns.get_loc(ticker)] * qtt_
         ltp = results_current.iloc[index, results_current.columns.get_loc(ticker)]


         # print(ticker,"qtt_",int(qtt_) * ltp ,"invesh",  ltp ,"ltp", results_current.iloc[index, results_current.columns.get_loc(ticker)])
         #
         #

         return invesh








    # #
    #
    #
    # return invesh


def stock_high_percentage(stock_df, ticker, index, column, percentage):



    if index > 0:
        # stock_df_lave = pd.DataFrame(entry_list_Holding).round(2)


        # breakpoint()

        new_value = (stock_df.iloc[index, column] * percentage / 100)
        # print(ticker, "shisft",stock_df.iloc[index -1, column].round(2), "ltp", stock_df.iloc[index, column].round(2))

        columns = ["Ticker", "start_date", "start_price", "end_date", "end_price","high", "Change", "Percentage",
                   "Percentage_HIGH","Rank_PARSENT", "invested"]

        results_last =pd.DataFrame(results, columns=columns)


        df_results_last= results_last.loc[(results_last['Ticker'] == ticker) ]
        df_results_last =  df_results_last.drop_duplicates(subset=['Ticker'], keep='last')

        # print(df_results_last)
        # #
        # # print("column",df_results_last.columns.get_loc("Percentage"))
        #
        # print("shisft",df_results_last.iloc[0, df_results_last.columns.get_loc("high")])
        # results_current = pd.DataFrame(results, columns=columns)
        results_current = pd.DataFrame(stock_df)
        results_current.reset_index()
        # print(results_current.head(10))

        # print("current", results_current.iloc[index,  results_current.columns.get_loc(ticker)])
        #

        # breakpoint()

        new_value = (df_results_last.iloc[0, df_results_last.columns.get_loc("high")]  * percentage / 100)



        if df_results_last.iloc[0, df_results_last.columns.get_loc("high")]  <  results_current.iloc[index,  results_current.columns.get_loc(ticker)] - new_value:
            high = results_current.iloc[index,  results_current.columns.get_loc(ticker)]

            # print("high","index", index, "column", ticker,
            #       "shisft", df_results_last.iloc[0, df_results_last.columns.get_loc("high")],
            #       "current", results_current.iloc[index, results_current.columns.get_loc(ticker)],
            #          "high" ,high                      )
            # breakpoint()




        else:

              high = df_results_last.iloc[0, df_results_last.columns.get_loc("high")]

              # print("low", "index", index, "column", ticker,
              #       "shisft", df_results_last.iloc[0, df_results_last.columns.get_loc("high")],
              #       "current", results_current.iloc[index, results_current.columns.get_loc(ticker)],
              #       "high", high)


        return high


    if index == 0:
        df = stock_df.iloc[index, column]
    # if index == 3:
    #       breakpoint()
    #


    return df





# print(yfinance_download)


# breakpoint()




# Fetch and process data for each ticker
count_index = 0


# print( start_price_limi)


for  Date in yfinance_download.index :


        cunt = cunt - 1

        if Date:



          print("Date total",len(yfinance_download.index),len(yfinance_download.index) - count_index,"Date",Date)

          # print(symbol_list)
          columns_count = 0
          for symbol in symbol_list:



            ticker  = symbol

            start_date = yfinance_download.index[0]
            start_price = yfinance_download.loc[yfinance_download.index[0], symbol]
            end_date = Date
            end_price = yfinance_download.loc[Date, symbol]

            entry_buy_df = yfinance_download.fillna(value=0.00)
            high = stock_high_percentage(stock_df=entry_buy_df, ticker= ticker,
                            index=count_index, column=columns_count, percentage=percentage_high)

            invesh =stock_invesh(stock_df=entry_buy_df, ticker= ticker,
                            index=count_index, column=columns_count, percentage=percentage_high)




            change = end_price - start_price
            pct_change = (change / start_price) * 100



            pct_change_high = (high - start_price) / start_price * 100
            Rank_PARSENT= 0
            invested = invesh




            # Append the results




            results.append([ticker,str(start_date),start_price, str(end_date),end_price, high, change, pct_change,

                            pct_change_high,Rank_PARSENT, invested,])

            columns_count = 1 + columns_count
        count_index = count_index + 1


#
columns = ["Ticker", "start_date", "start_price", "end_date", "end_price", "high", "Change", "Percentage",
           "Percentage_HIGH","Rank_PARSENT", "invested"]
df_results = pd.DataFrame(results, columns=columns)


df = pd.DataFrame(df_results)
# print(df)


# df_results=df_results.loc[(df_results["start_price"] < start_price_limit)]


#

# df_results["Rank_PARSENT"] = df_results["Percentage"].rank(ascending=0)
# df_results.sort_values("Ticker", axis=0, ascending=True, inplace=True)

# df_results["Balance"] = Balance

df_results["qtt"] = (df_results["invested"] / df_results["start_price"]).astype(int)
df_results["invested total"] = df_results.groupby("Ticker")["invested"].cumsum()


# Group by 'Category' and calculate cumulative sum
# df['Cumulative_Sum'] = df.groupby('Category')['Value'].cumsum()
df_results["qtt total"] = df_results.groupby("Ticker")["qtt"].cumsum()



df_results["price_avej"] =df_results["invested total"] / df_results["qtt total"]
df_results["ltp"] = df_results["end_price"]


df_results["sell invested"] = df_results["qtt total"] * df_results["end_price"]

df_results["Change invested"] = df_results["sell invested"] - df_results["invested total"]

# df_results['invested cummax'] = df_results["invested"].cumsum()
# df_results['sell inves cummax'] = df_results["qtt"].cumsum() *  df_results["end_price"]#df_results["qtt"]
# df_results['Change cummax'] =df_results["Change invested"] .cumsum()
df_results['Percentage cummax'] = (df_results['Change invested'] / df_results["invested total"]) * 100


# unique=df_results.columns
#
#
print(df_results.round(2))
#
# print(unique)

# df = pd.DataFrame(columns=unique)

final_output=[]

for Ticker in df_results["Ticker"].unique():
    # print(Ticker)

    df_results =pd.DataFrame (df_results )
    df_results_last_ = df_results.loc[(df_results['Ticker'] == Ticker)]
    df_results_last = df_results_last_.drop_duplicates(subset=['Ticker'], keep='last')

    # print(  df_results_last_)
    #
    # breakpoint()



    start_date =        df_results_last.iloc[0, df_results_last.columns.get_loc("start_date")]    #
    start_price =       df_results_last.iloc[0, df_results_last.columns.get_loc("start_price")]  #

    end_date =          df_results_last.iloc[0, df_results_last.columns.get_loc("end_date")]    #df_results["end_date"][0]
    end_price =         df_results_last.iloc[0, df_results_last.columns.get_loc("end_price")]
    high =              df_results_last.iloc[0, df_results_last.columns.get_loc("high")]
    change =            df_results_last.iloc[0, df_results_last.columns.get_loc("Change")]
    Percentagee =        df_results_last.iloc[0, df_results_last.columns.get_loc("Percentage")]
    Percentage_high =   df_results_last.iloc[0, df_results_last.columns.get_loc("Percentage_HIGH")]
    Rank_PARSENT =      df_results_last.iloc[0, df_results_last.columns.get_loc("Rank_PARSENT")]
    invested =          df_results_last_["invested"].sum()
    qtt =               df_results_last_["qtt"].sum().astype(int)
    sell_invested =     qtt  *  df_results_last.iloc[0, df_results_last.columns.get_loc("end_price")]
    Change_invested=    sell_invested - invested
    Percentage_net =    (Change_invested / invested) * 100

    # qtt = df_results_last_["Change invested"].sum()

    final_output.append([Ticker, str(start_date), start_price, str(end_date), end_price, high, change, Percentagee,

                    Percentage_high, Rank_PARSENT, invested,qtt,sell_invested,Change_invested ,Percentage_net])
    # print(final_output)





columns = ["Ticker", "start_date", "start_price", "end_date", "end_price", "high", "Change", "Percentage",
           "Percentage_HIGH", "Rank_PARSENT", "invested",
           "qtt","sell_invested","Change_invested ","Percentage_net"
                                          ]


final_results = pd.DataFrame(final_output, columns=columns)

final_results['invested_total'] =final_results["invested"] .cumsum()
final_results['sell_invested_total'] =final_results["sell_invested"] .cumsum()
final_results['Change_invested'] =final_results['sell_invested_total'] - final_results['invested_total']





final_results['Percentage_total'] = (final_results['Change_invested'] / final_results['invested_total']) * 100






print(final_results)
# breakpoint()




# #
# columns = ["Ticker", "start_date", "start_price", "end_date","end_price","Change", "Percentage","Rank_PARSENT",
#            "Balance", "qtt", "inves", "sell inves", "Change inves",'inves cummax','sell inves cummax','Change cummax','Percentage cummax',           ]
#
# df_results = pd.DataFrame(df_results, columns=columns)






df=pd.DataFrame()
import xlwings
Book_NAME = "data_NSC_ALL2.xlsx"


def print_sheets(df, sheets_name, range):
    ws = xlwings.Book(Book_NAME).sheets(sheets_name)
    ws.range(range).value = pd.DataFrame(df.round(2))


df_results=df_results.loc[(df_results["Ticker"] == "SUZLON.NS")]
dp.print_sheets(df=df_results, sheets_name="NSE", range="A5")


# Save the results to a CSV file
df_results.to_csv("nse_stock_changes.csv", index=False)




