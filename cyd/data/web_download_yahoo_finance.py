#-*- coding: utf-8 -*-

import requests
import io
import pandas as pd

# https://query1.finance.yahoo.com/v7/finance/download/PLTR?period1=1644765745&period2=1676301745&interval=1d&events=history&includeAdjustedClose=true

import datetime


def convert_date_str_timestampe(date_str):
    # start_date_str = "2022-02-13"
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    date_ts = int(datetime.datetime.timestamp(date))
    return date_ts


def download_data(stock_id, start_date_str="2022-01-01", end_date_str="2023-01-01"):
    session = requests.Session()
    # 使用我的代理
    session.proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }

    start_ts = convert_date_str_timestampe(start_date_str)
    end_ts = convert_date_str_timestampe(end_date_str)
    url = "https://query1.finance.yahoo.com/v7/finance/download/{stock_id}?period1={start_ts}&period2={end_ts}&interval=1d&events=history&includeAdjustedClose=true".format(
        stock_id=stock_id,
        start_ts=start_ts,
        end_ts=end_ts)
    # print(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    resp = session.get(url, headers=headers)
    print(session.headers)
    content = resp.content.decode('utf-8')
    # print(content)
    dataframe = pd.read_csv(io.StringIO(content), sep=',')
    return dataframe

def save_tick_to_csv():
    tick_id='AGG'
    start_date_str = '1998-01-01'
    end_date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    tick_df = download_data(stock_id=tick_id, start_date_str=start_date_str, end_date_str=end_date_str)

    tick_df.to_csv('D:/QSTRADER_DATA/data/{tick_name}.csv'.format(tick_name=tick_id), index=False,encoding='utf-8-sig')

def save_tick_list_to_csv():
    strategy_symbols = ['XL%s' % sector for sector in "BCEFIKPUVY"]

    strategy_symbols = ["SPY", "IJS", "EFA", "EEM", "AGG", "JNK", "DJP", "RWR"]
    for symbol in strategy_symbols:
        tick_id = symbol
        start_date_str = '1998-01-01'
        end_date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        tick_df = download_data(stock_id=tick_id, start_date_str=start_date_str, end_date_str=end_date_str)

        tick_df.to_csv('D:/QSTRADER_DATA/data/{tick_name}.csv'.format(tick_name=tick_id), index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    #save_tick_to_csv()
    save_tick_list_to_csv()
