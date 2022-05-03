# -*- coding:utf-8 -*-
"""
@Time : 2022/5/3 17:17
@Author: windatlantis
@File : MacdDeviation.py
"""

import pandas as pd
from pandas import DataFrame
from datetime import datetime

from main.domain import DataCreator


def deviation_day_15min(stock_id, read_csv=True):
    day_macd, day_macd_data = DataCreator.get_one_year_macd(stock_id, read_csv)
    min15_macd, min15_macd_data = DataCreator.get_one_year_macd(stock_id, read_csv, frequency='15')
    min5_macd, min5_macd_data = DataCreator.get_one_year_macd(stock_id, read_csv, frequency='5')
    deviation_day_15min_buy1(day_macd, min15_macd_data)


def deviation_day_15min_buy1(day_macd: DataFrame, min15_macd_data: DataFrame):
    # 买入信号1：日线macd金叉，且开口向上，15分钟金叉，在0轴或0轴以下。
    day_macd_positive = []
    min15_macd_buy = pd.DataFrame(columns=['date', 'time', 'close'])
    # 日线
    line_num = day_macd.shape[0]
    for i in range(line_num):
        cur = day_macd.iloc[i]
        # 日线macd金叉,macd不断变大
        if i > 0 and cur['macd'] > 0 and cur['macd'] > day_macd.iloc[i - 1]['macd']:
            day_macd_positive.append(cur['date'])
    # 15分钟线

    for day in day_macd_positive:
        # 日线macd金叉
        temp = min15_macd_data[min15_macd_data['date'] == day]
        line_num = temp.shape[0]
        for i in range(line_num):
            cur = temp.iloc[i]
            # 15分钟金叉，在0轴或0轴以下
            if i > 0 and cur['macd'] > 0 and cur['macd'] > temp.iloc[i - 1]['macd'] and cur['dif'] <= 0:
                min15_macd_buy.loc[min15_macd_buy.shape[0]] = [day, get_hhmmss(cur['time']), cur['close']]
    print(min15_macd_buy)


def get_hhmmss(time):
    new_time = datetime.strptime(str(time)[8:-3], '%H%M%S')
    return new_time.strftime('%H:%M:%S')
