# -*- coding:utf-8 -*-
"""
@Time : 2022/5/14 15:54
@Author: windatlantis
@File : Day15mStrategy.py
"""
from datetime import datetime

from pandas import DataFrame

from main.domain import DataCreator
import pandas as pd

def day_15min_golden_cross(stock_id, read_csv=True):
    """
    日-15金叉套
    :param stock_id:
    :param read_csv:
    :return:
    """
    day_macd, day_macd_data = DataCreator.get_one_year_macd(stock_id, read_csv)
    min15_macd, min15_macd_data = DataCreator.get_one_year_macd(stock_id, read_csv, frequency='15')
    min5_macd, min5_macd_data = DataCreator.get_one_year_macd(stock_id, read_csv, frequency='5')
    day_15min_buy1(day_macd, min15_macd_data)


def day_15min_buy1(day_macd: DataFrame, min15_macd_data: DataFrame):
    """
    买入信号1：日线macd金叉，且开口向上，15分钟金叉，在0轴或0轴以下。
    :param day_macd:
    :param min15_macd_data:
    :return:
    """
    days = __collect_golden_cross_day(day_macd)
    min15_macd_buy = pd.DataFrame(columns=['date', 'time', 'close'])

    for day in days:
        # 日线macd金叉
        # 15分钟线
        temp = min15_macd_data[min15_macd_data['date'] == day]
        line_num = temp.shape[0]
        for i in range(line_num):
            cur = temp.iloc[i]
            # 15分钟金叉，在0轴或0轴以下
            if __macd_golden_cross(i, cur, temp) and cur['dif'] <= 0:
                min15_macd_buy.loc[min15_macd_buy.shape[0]] = [day, __get_hhmmss(cur['time']), cur['close']]
    print(min15_macd_buy)


def day_15min_buy2(day_macd: DataFrame, min15_macd_data: DataFrame, min5_macd_data: DataFrame):
    """
    买入信号2：日线macd金叉且开口向上，15分钟即将金叉，5分钟级别底背离，在0轴或0轴以下
    :param day_macd:
    :param min15_macd_data:
    :param min5_macd_data:
    :return:
    """
    days = __collect_golden_cross_day(day_macd)
    min15_macd_buy = pd.DataFrame(columns=['date', 'time', 'close'])

    for day in days:
        # 日线macd金叉
        # 15分钟线
        temp = min15_macd_data[min15_macd_data['date'] == day]
        line_num = temp.shape[0]
        for i in range(line_num):
            cur = temp.iloc[i]
            # 15分钟即将金叉，在0轴或0轴以下
            if __macd_golden_cross(i, cur, temp) and cur['dif'] <= 0:
                min15_macd_buy.loc[min15_macd_buy.shape[0]] = [day, __get_hhmmss(cur['time']), cur['close']]
    print(min15_macd_buy)


def __macd_golden_cross(idx, data: DataFrame, history: DataFrame):
    """
    macd金叉，且开口向上
    :param idx:
    :param data:
    :param history:
    :return:
    """
    return idx > 0 and data['macd'] > 0 and data['macd'] > history.iloc[idx - 1]['macd']


def __collect_golden_cross_day(day_macd: DataFrame):
    """
    收集日线macd金叉日期
    :param day_macd:
    :return:
    """
    days = []
    line_num = day_macd.shape[0]
    for i in range(line_num):
        cur = day_macd.iloc[i]
        # 日线macd金叉,macd不断变大
        if __macd_golden_cross(i, cur, day_macd):
            days.append(cur['date'])
    return days


def __get_hhmmss(time):
    """
    把日期+时间转为时间
    :param time:
    :return:
    """
    new_time = datetime.strptime(str(time)[8:-3], '%H%M%S')
    return new_time.strftime('%H:%M:%S')
