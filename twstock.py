import pandas as pd
import requests
from io import StringIO
import time
def monthly_report(year, month):
    
    # 
    if year > 1990:
        year -= 1911
    
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
    if year <= 98:
        url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
    
    # 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # 
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'

    dfs = pd.read_html(StringIO(r.text), encoding='big-5')

    df = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])
    
    
    info_columns = ["revenue", "revenueLastMonth"]
    stk_list = []
    stk_info_df = pd.DataFrame(index = stk_list, columns = info_columns)
    
    if 'levels' in dir(df.columns):
        print("====levels====")
        df.columns = df.columns.get_level_values(1)
    else:
        df = df[list(range(0,10))]
        column_index = df.index[(df[0] == '公司代號')][0]
        df.columns = df.iloc[column_index]
    
    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    #df = df[~df['當月營收'].isnull()]
    
    df = df[(df['當月營收'] > 100000)]
    
    # df = df[df['公司代號'] != '合計']
    
    # 
    time.sleep(5)

    return df

from datetime import date
today = date.today()
month = int(today.month)
year = int(today.year)
day = int(today.day)
month -= 1
if day > 10:
    month -= 1
if month <= 0:
    year-=1
    month+=12
print(today)
monthly_report(year,month).to_csv('twstock.csv')
info_columns = ["revenue", "mom", "yoy"]

import csv
with open('twstock.csv', 'r') as csvfile:
    rows = csv.reader(csvfile)
    new_rows = dict()
    number = 1
    tickers = []
    for tk in rows:
        if tk[1].isnumeric():
            revenue = tk[3]
            mom = float(tk[6])
            yoy = float(tk[7])
            number+=1
            if mom > 0.0 and yoy > 0.0:
                tickers.append(tk[1])
                new_rows[tk[1]] =  list([revenue, mom, yoy])

    stk_info_df = pd.DataFrame(index = tickers, columns = info_columns)
    
    for tk in tickers:
        stk_info_df.loc[tk]["revenue"] = new_rows[tk][0]
        stk_info_df.loc[tk]["mom"] = new_rows[tk][1]
        stk_info_df.loc[tk]["yoy"] = new_rows[tk][2]
    
    # with open('tw_final.csv', 'w') as f:
        # writer = csv.writer(f)
        # for k, v in new_rows.items():
            # writer.writerow([k, v])

stk_info_df.to_csv('tw_final_out.csv')