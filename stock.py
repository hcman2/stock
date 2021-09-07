import requests
import pandas as pd

import yfinance as yf
import time

#stk_list = {"AAPL","TSLA","MSFT"}
#stock = yf.Ticker('AAPL')
#stock.financials.to_csv('profit_loss_account_AAPL2.csv')
#stock.balance_sheet.to_csv('balance_sheet_AAPL2.csv')
import macroeconomics as eco

eco_result = eco.economic_trend()
print(eco_result)
#eco score = nonfarm + gdp - GS10
eco_score = eco_result[0] + eco_result[1] - eco_result[2]

#input('pause:')
info_columns = ["currentPrice", "targetMeanPrice", "forwardEps", "recommendationMean", "earningsGrowth", "revenueGrowth"]
failed_list = []
stk_list = []
import csv
with open('stock_list.csv', 'r') as csvfile:
    rows = csv.reader(csvfile)    
    for tk in rows:
        stk_list.append(tk[0])
        
stk_info_df = pd.DataFrame(index = stk_list, columns = info_columns)        
stk_suggest = pd.DataFrame(index = stk_list, columns = ["score"])
for i in stk_info_df.index:
    try:
        print('processing: ' + i)
        stock = yf.Ticker(i)
        info_dict = stock.info
        columns_included = list(info_dict.keys())
        #print(columns_included)
        #input('pause:')
        intersect_columns = [x for x in info_columns if x in columns_included]
        stk_info_df.loc[i,intersect_columns] = list(pd.Series(info_dict)[intersect_columns].values)
        #earning = stock.quarterly_earnings.tail(5)
        #stock.quarterly_financials
        #stock.quarterly_cashflow
        time.sleep(2)
    except:
        failed_list.append(i)
######
#stock god core algo
######   
#fill zero for empty slots
stk_info_df = stk_info_df.fillna(0)
no_predict_list = []
for i in stk_info_df.index:
    try:
        currPrice = stk_info_df.loc[i,"currentPrice"]
        print('current price')
        print(currPrice)
        targPrice = stk_info_df.loc[i,"targetMeanPrice"]
        score = 0
        #In this part you have to implement your formula to get the score of a ticker
        if targPrice != 0:
            score = (targPrice - currPrice)/currPrice
            print('initial score: ')
            print(score)
            if eco_score > 0:
                if score > eco_score:
                    score = 0.5*score+0.5*eco_score
            else:
                score = 0.8*score+0.2*eco_score
            print('adjusted score 1: ')
            print(score)
        earningsGrowth = stk_info_df.loc[i,"earningsGrowth"]
        revenueGrowth = stk_info_df.loc[i,"revenueGrowth"]
        if earningsGrowth != 0 and revenueGrowth!= 0:
            if earningsGrowth<0.1 and revenueGrowth<0.1 and score > 0:
                score = 0.8*score
            if earningsGrowth>0.1 and revenueGrowth>0.1 and score < 0:
                score = 0
            print('adjusted score 2: ')
            print(score)
        stk_suggest.loc[i,"score"] = score
    except:
        stk_suggest.loc[i,"score"] = -100
        no_predict_list.append(i)

stk_info_df.to_csv('out.csv')
stk_suggest.to_csv('score.csv')
print('failed to fetch stock data list:')
print(failed_list)
print('no predict result list:')
print(no_predict_list)


