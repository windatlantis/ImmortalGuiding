# -*- coding:utf-8 -*-
"""
@Time : 2022/5/14 15:54
@Author: windatlantis
@File : Day15mStrategy.py
"""
from datetime import datetime

from pandas import DataFrame

from main.domain import DataCreator
from main.service import LineCrossService, DeviationService
from main.utils import CollectionUtil, FileUtil, DateUtil
import pandas as pd

min5 = 500000
min15 = min5 * 3
k_type_date_list = ['m', 'w', 'd']
k_type_time_list = ['60m', '15m', '5m']
k_type_time_map = {
    'm': 'date',
    'w': 'date',
    'd': 'date',
    '60m': 'time',
    '15m': 'time',
    '5m': 'time',
}


def day_15min(stock_id, read_csv=True):
    """
    日-15金叉套
    :param stock_id:
    :param read_csv:
    :return:
    """
    # 买卖记录
    record_list = pd.DataFrame(columns=['date', 'time', 'price', 'operation'])
    day_macd, day_macd_data = DataCreator.get_half_year_macd(stock_id, read_csv)
    min15_macd, min15_macd_data = DataCreator.get_half_year_macd(stock_id, read_csv, frequency='15')
    min5_macd, min5_macd_data = DataCreator.get_half_year_macd(stock_id, read_csv, frequency='5')

    for i in range(3, day_macd_data.shape[0]):
        cur = day_macd_data.iloc[i]
        last = day_macd_data.iloc[i - 1]
        # 日期
        day = cur['date']
        print('day:' + day)
        # 今天及前3天
        date_range = DateUtil.get_date_range(day, -3)
        # 日线macd金叉及其延申
        golden_cross_day = cur['macd'] > 0 and cur['macd'] >= last['macd']
        # 5分钟级别macd
        macd_5 = pd.DataFrame(columns=min5_macd_data.columns)
        # 15分钟级别macd
        macd_15 = pd.DataFrame(columns=min15_macd_data.columns)
        for j in range(len(date_range)):
            CollectionUtil.df_add(macd_5, min5_macd_data[min5_macd_data['date'] == date_range[j]])
            CollectionUtil.df_add(macd_15, min15_macd_data[min15_macd_data['date'] == date_range[j]])
        # 15分钟级别金叉死叉
        line_cross_15 = LineCrossService.line_cross(macd_15, date_name='time')
        # 5分钟级别金叉死叉
        line_cross_5 = LineCrossService.line_cross(macd_5, date_name='time')
        # 5分钟级别背离
        macd_deviation_5 = DeviationService.collect_macd_deviation(line_cross_5, date_name='time')
        if golden_cross_day:
            day_15min_buy1(day, line_cross_15, record_list)
            day_15min_buy2(day, line_cross_15, macd_deviation_5, record_list)
        day_15min_sell(day, macd_15, line_cross_15, line_cross_5, macd_deviation_5, record_list)
    record_list = handle_record(record_list)
    print(record_list)
    FileUtil.write_csv(record_list, 'record_list_{}'.format(stock_id))


def handle_record(record_list):
    record_list = record_list.sort_values('time')
    tips = []
    stocks = []
    stock = 0
    for j in range(record_list.shape[0]):
        cur = record_list.iloc[j]
        last = record_list.iloc[j - 1]
        tip = ''
        if 'sell' in cur['operation']:
            if stock == 0:
                tip = 'buy first'
            else:
                stock = 0
        elif 'buy' in cur['operation']:
            stock += 1
        if j > 1 and len(tip) == 0 and len(cur['operation']) == len(last['operation']):
            tip = 'repeat'
        tips.append(tip)
        stocks.append(stock)
    record_list.insert(record_list.shape[1], 'tips', tips)
    record_list.insert(record_list.shape[1], 'stocks', stocks)
    return record_list


def day_15min_buy1(day, line_cross_15: DataFrame, record_list):
    """
    买入信号1：日线macd金叉，且开口向上，15分钟金叉，在0轴或0轴以下。
    :param day:
    :param line_cross_15:
    :param record_list:
    :return:
    """
    if line_cross_15.empty:
        return
    # 15分钟线金叉
    golden_cross = line_cross_15[(line_cross_15['cross_type'] == 'golden') & (line_cross_15['true_cross'] == True)]
    if golden_cross.empty:
        return
    for i in range(golden_cross.shape[0]):
        cur = golden_cross.iloc[i]
        # 在0轴或0轴以下
        if cur['zero_axis'] <= 0 and cur['time'] == day:
            __add_to_record_list(record_list, [day, cur['time'], cur['close'], "buy1"])


def day_15min_buy2(day, line_cross_15: DataFrame, macd_deviation_5: DataFrame, record_list):
    """
    买入信号2：日线macd金叉且开口向上，15分钟即将金叉，在0轴或0轴以下，5分钟级别底背离
    :param day:
    :param line_cross_15:
    :param macd_deviation_5:
    :param record_list:
    :return:
    """
    if line_cross_15.empty or macd_deviation_5.empty:
        return
    golden_cross_15 = line_cross_15[line_cross_15['cross_type'] == 'golden_soon']
    bottom_deviation_5 = macd_deviation_5[macd_deviation_5['deviation_type'] == 'bottom']
    if golden_cross_15.empty or bottom_deviation_5.empty:
        return
    for i in range(golden_cross_15.shape[0]):
        cur = golden_cross_15.iloc[i]
        # 在0轴或0轴以下
        if cur['zero_axis'] <= 0 and cur['date'] == day:
            cur_time = cur['time']
            deviation_5 = bottom_deviation_5[
                (cur_time - min15 < bottom_deviation_5['time']) & (bottom_deviation_5['time'] <= cur_time)]
            if not deviation_5.empty:
                __add_to_record_list(record_list,
                                     [day, deviation_5.iloc[0]['time'], deviation_5.iloc[0]['close'], "buy2"])


def day_15min_sell(day, macd_15: DataFrame, line_cross_15: DataFrame, line_cross_5: DataFrame,
                   macd_deviation_5: DataFrame, record_list):
    """
    卖出信号：15分钟级别，在0轴以下，5分钟死叉。在0轴以上，15分钟即将死叉，5分钟顶背离。
    :param day:
    :param macd_15:
    :param line_cross_15:
    :param line_cross_5:
    :param macd_deviation_5:
    :param record_list:
    :return:
    """
    dead_cross_5 = line_cross_5[(line_cross_5['cross_type'] == 'dead') & (line_cross_5['true_cross'] == True)]
    dead_cross_soon_15 = line_cross_15[line_cross_15['cross_type'] == 'dead_soon']
    top_deviation_5 = macd_deviation_5[macd_deviation_5['deviation_type'] == 'top']
    for i in range(macd_15.shape[0]):
        cur = macd_15.iloc[i]
        if not cur['date'] == day:
            continue
        cur_time = cur['time']
        if cur['macd'] < 0:
            dead_5 = dead_cross_5[(cur_time - min15 < dead_cross_5['time']) & (dead_cross_5['time'] <= cur_time)]
            if not dead_5.empty:
                __add_to_record_list(record_list, [day, dead_5.iloc[0]['time'], dead_5.iloc[0]['close'], "sell1"])
        elif cur_time in dead_cross_soon_15['time']:
            top_5 = top_deviation_5[
                (cur_time - min15 < top_deviation_5['time']) & (top_deviation_5['time'] <= cur_time)]
            if not top_5.empty:
                __add_to_record_list(record_list, [day, top_5.iloc[0]['time'], top_5.iloc[0]['close'], "sell2"])


def __add_to_record_list(record_list: DataFrame, data):
    # op = data[-1]
    # tip = ''
    # if record_list.empty and 'sell' in op:
    #     tip = 'buy first'
    # if not record_list.empty:
    #     last = record_list.iloc[-1]
    #     if len(last[-2]) == len(op):
    #         tip = 'repeat'
    # data.append(tip)
    CollectionUtil.df_add(record_list, data)


def __get_hhmmss(time):
    """
    把日期+时间转为时间
    :param time:
    :return:
    """
    new_time = datetime.strptime(str(time)[8:-3], '%H%M%S')
    return new_time.strftime('%H:%M:%S')
