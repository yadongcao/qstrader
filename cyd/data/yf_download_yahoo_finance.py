#-*- coding: utf-8 -*-

import yfinance as yf
from datetime import datetime
import requests

session = requests.Session()
# 使用我的代理
session.proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

def download():
    # CREATE TICKER INSTANCE FOR AMAZON
    tick_name_str='GLD'
    start_date_str='2001-01-01'
    tick = yf.Ticker(tick_name_str, session=session)
    # GET TODAYS DATE AND CONVERT IT TO A STRING WITH YYYY-MM-DD FORMAT (YFINANCE EXPECTS THAT FORMAT)
    end_date = datetime.now().strftime('%Y-%m-%d')
    data_hist = tick.history(start=start_date_str, end=end_date)
    data_hist.to_csv('D:/QSTRADER_CSV_DATA/{tick_name}.csv'.format(tick_name=tick_name_str), index=False, encoding='utf-8-sig')



if __name__ == '__main__':
    download()