import requests
import pandas as pd

import yfinance as yf
import time

#stk_list = {"AAPL","TSLA","MSFT"}
#stock = yf.Ticker('AAPL')
#stock.financials.to_csv('profit_loss_account_AAPL2.csv')
#stock.balance_sheet.to_csv('balance_sheet_AAPL2.csv')


#fetch economic research
from fredapi import Fred
import datetime as dt

api_key = 'fb88f90f5fc4526e3df86df73873a487'
fred = Fred(api_key)

#test code
#gdp_data=fred.get_series('GDP')
#nonfarm_data = fred.get_series('PAYEMS')
#tbond_data = fred.get_series('GS10')
#nonfarm data is monthly
#gdp data is quaterly

def calculate_extrapolation(data):
    sz = data.size
    y3 = data[sz-1]
    y2 = data[sz-2]
    y1 = data[sz-3]
    y0 = data[sz-4]
    c0 = y0
    c3 = (y3-3*y2+3*y1-y0)/6
    c2 = (-y3+4*y2-5*y1+2*y0)/2
    c1 = y1 - c3 - c2 - c0
    #print(data)
    #print(c0)
    #print(c0+c1+c2+c3)
    #print(c0+2*c1+4*c2+8*c3)
    #print(c0+3*c1+9*c2+27*c3)
    result = []
    result.append(c0)
    result.append(c1)
    result.append(c2)
    result.append(c3)
    return c0+4*c1+16*c2+64*c3

#print("Non-Farm data prediction....")
#print(nonfarm_data.tail(1))
#nonfarm_data = nonfarm_data.tail(4)
#nonfarm_data = nonfarm_data.to_numpy()
#pred = calculate_extrapolation(nonfarm_data)
#nonfarm_ratio = (pred-nonfarm_data[-1])/nonfarm_data[-1]*100
#
#print("GDP data prediction....")
#print(gdp_data.tail(1))
#gdp_data = gdp_data.tail(4)
#gdp_data = gdp_data.to_numpy()
#pred = calculate_extrapolation(gdp_data)
#gdp_ratio = (pred-gdp_data[-1])/gdp_data[-1]*100
#
#print("Treasury Bonds data prediction....")
#print(tbond_data.tail(1))
#tbond_data = tbond_data.tail()
#tbond_data = tbond_data.to_numpy()
#pred = calculate_extrapolation(tbond_data)
#tbond_ratio = (pred-tbond_data[-1])/tbond_data[-1]*100

#input('pause:')
info_columns = ["targetMeanPrice", "forwardEps", "recommendationMean", "earningsGrowth", "revenueGrowth"]
failed_list = []
stk_list = []
import csv
with open('stock_list.csv', 'r') as csvfile:
    rows = csv.reader(csvfile)    
    for tk in rows:
        stk_list.append(tk[0])
        
stk_info_df = pd.DataFrame(index = stk_list, columns = info_columns)        

for i in stk_info_df.index:
    try:
        print('processing: ' + i)
        stock = yf.Ticker(i)
        info_dict = stock.info
        columns_included = list(info_dict.keys())
        intersect_columns = [x for x in info_columns if x in columns_included]
        stk_info_df.loc[i,intersect_columns] = list(pd.Series(info_dict)[intersect_columns].values)
        #earning = stock.quarterly_earnings.tail(5)
        #print(columns_included)
        #stock.quarterly_financials
        #stock.quarterly_cashflow
        time.sleep(1)
    except:
        failed_list.append(i)
        
stk_info_df.to_csv('out.csv')
print('failed list:')
print(failed_list)


