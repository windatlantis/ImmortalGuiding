# -*- coding:utf-8 -*-
"""
@Time : 2022/5/14 15:54
@Author: windatlantis
@File : Day15mStrategy.py
"""
from datetime import datetime

from pandas import DataFrame

from main.domain import DataCreator, Analysiser
from main.service import LineCrossService, DeviationService
from main.utils import CollectionUtil, FileUtil, DateUtil
import pandas as pd

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
    record_list = pd.DataFrame(columns=['date', 'time', 'price', 'operation', 'zero_axis_60'])
    day_macd, day_macd_data = DataCreator.get_half_year_macd(stock_id, read_csv)
    min60_macd, min60_macd_data = DataCreator.get_half_year_macd(stock_id, read_csv, frequency='60')
    min15_macd, min15_macd_data = DataCreator.get_half_year_macd(stock_id, read_csv, frequency='15')
    min5_macd, min5_macd_data = DataCreator.get_half_year_macd(stock_id, read_csv, frequency='5')

    # # 5分钟级别金叉死叉
    # line_cross_5 = LineCrossService.line_cross(min5_macd_data, date_name='time')
    # # 5分钟级别背离
    # macd_deviation_5 = DeviationService.collect_macd_deviation(line_cross_5, date_name='time')
    # FileUtil.write_csv(macd_deviation_5, 'macd_deviation_5_{}'.format(stock_id))

    sell_model_1 = True
    for i in range(20, day_macd_data.shape[0]):
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
        # 当天15分钟级别macd
        macd_15_day = min15_macd_data[min15_macd_data['date'] == day]
        # 当天60分钟级别macd
        macd_60_day = min60_macd_data[min60_macd_data['date'] == day]
        # 15分钟级别金叉死叉
        line_cross_15 = LineCrossService.line_cross(macd_15, date_name='time')
        line_cross_soon_15 = LineCrossService.line_cross_soon(macd_15, date_name='time')
        # 5分钟级别金叉死叉
        line_cross_5 = LineCrossService.line_cross(macd_5, date_name='time')
        # 5分钟级别背离
        macd_deviation_5 = DeviationService.collect_macd_deviation(line_cross_5, date_name='time')

        # 日线macd金叉及其延申
        if golden_cross_day:
            day_15min_buy1(day, line_cross_15, macd_60_day, record_list)
            day_15min_buy2(day, line_cross_soon_15, macd_deviation_5, macd_60_day, record_list)

        if sell_model_1:
            # 卖出模式1
            sell_model_1 = day_15min_sell(day, macd_15_day, line_cross_5, line_cross_soon_15, macd_deviation_5,
                                          line_cross_15, macd_60_day, record_list)
        if not sell_model_1:
            # 卖出模式2
            # 60分钟级别macd
            macd_60 = pd.DataFrame(columns=min60_macd_data.columns)
            for j in range(len(date_range)):
                CollectionUtil.df_add(macd_60, min60_macd_data[min60_macd_data['date'] == date_range[j]])
            # 60分钟级别金叉死叉
            line_cross_60 = LineCrossService.line_cross(macd_60, date_name='time')
            line_cross_soon_60 = LineCrossService.line_cross_soon(macd_60, date_name='time')
            # 15分钟级别背离
            macd_deviation_15 = DeviationService.collect_macd_deviation(line_cross_15, date_name='time')
            day_60min_sell(day, macd_60_day, line_cross_60, line_cross_soon_60, macd_deviation_15, record_list)

    record_list = handle_record(record_list)
    print(record_list)
    Analysiser.save_record(record_list, stock_id)


def handle_record(record_list):
    """
    处理买卖记录
    :param record_list:
    :return:
    """
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


def day_15min_buy1(day, line_cross_15: DataFrame, macd_60_day, record_list):
    """
    买入信号1：日线macd金叉，且开口向上，15分钟金叉，在0轴或0轴以下。
    :param day:
    :param line_cross_15:
    :param macd_60_day:
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
        if cur['zero_axis'] <= 0 and cur['date'] == day:
            cur_time = cur['time']
            zero_axis_60 = \
                macd_60_day[
                    (DateUtil.calculate_time(cur_time, 60) > macd_60_day['time']) & (cur_time <= macd_60_day['time'])][
                    'dif'].iloc[0]
            __add_to_record_list(record_list, [day, cur_time, cur['close'], "buy1", zero_axis_60])


def day_15min_buy2(day, line_cross_soon_15: DataFrame, macd_deviation_5: DataFrame, macd_60_day, record_list):
    """
    买入信号2：日线macd金叉且开口向上，15分钟即将金叉，在0轴或0轴以下，5分钟级别底背离
    :param day:
    :param line_cross_soon_15:
    :param macd_deviation_5:
    :param macd_60_day:
    :param record_list:
    :return:
    """
    if line_cross_soon_15.empty or macd_deviation_5.empty:
        return
    # 15分钟即将金叉
    golden_cross_15 = line_cross_soon_15[line_cross_soon_15['cross_soon_type'] == 'golden_soon']
    # 5分钟级别底背离
    bottom_deviation_5 = macd_deviation_5[macd_deviation_5['deviation_type'] == 'bottom']
    if golden_cross_15.empty or bottom_deviation_5.empty:
        return
    for i in range(golden_cross_15.shape[0]):
        cur = golden_cross_15.iloc[i]
        # 在0轴或0轴以下
        if cur['zero_axis'] <= 0 and cur['date'] == day:
            cur_time = cur['time']
            deviation_5 = bottom_deviation_5[
                (DateUtil.calculate_time(cur_time, -15) < bottom_deviation_5['time']) & (
                        bottom_deviation_5['time'] <= cur_time)]
            if not deviation_5.empty:
                zero_axis_60 = macd_60_day[
                    (DateUtil.calculate_time(cur_time, 60) > macd_60_day['time']) & (cur_time <= macd_60_day['time'])][
                    'dif'].iloc[0]
                __add_to_record_list(record_list,
                                     [day, deviation_5.iloc[0]['time'], deviation_5.iloc[0]['close'], "buy2",
                                      zero_axis_60])


def day_15min_sell(day, macd_15_day, line_cross_5, line_cross_soon_15, macd_deviation_5, line_cross_15,
                   macd_60_day, record_list):
    """
    卖出信号：15分钟级别
            - 在0轴以下，5分钟死叉。
            - 在0轴以上，15分钟即将死叉，5分钟顶背离。15分钟出现死叉一定卖出。
                * 如果15分钟把60分钟带上0轴，则改看60分钟信号。
                  即，15分钟买出信号出现时，60分钟MACD在0轴以下，15分钟卖出信号时，60分钟MACD在0轴以上了
                  变更卖出条件为：60分钟即将死叉，15分钟顶背离。如果未出现15分钟顶背离，则60分钟死叉卖出。
    :param day:
    :param macd_15_day:
    :param line_cross_5:
    :param line_cross_soon_15:
    :param macd_deviation_5:
    :param line_cross_15:
    :param macd_60_day:
    :param record_list:
    :return:
    """
    # 先买入才能卖出
    last_record = CollectionUtil.df_getlast(record_list, None)
    if last_record is None or 'sell' in last_record['operation']:
        return True
    # 加载条件*所需数据
    need_load_data = last_record['zero_axis_60'] < 0
    # 正常卖出条件
    dead_cross_5 = line_cross_5[(line_cross_5['cross_type'] == 'dead') & (line_cross_5['true_cross'] == True)]
    dead_cross_soon_15 = line_cross_soon_15[line_cross_soon_15['cross_soon_type'] == 'dead_soon']
    top_deviation_5 = macd_deviation_5[macd_deviation_5['deviation_type'] == 'top']
    dead_cross_15 = line_cross_15[(line_cross_15['cross_type'] == 'dead') & (line_cross_15['true_cross'] == True)]
    for i in range(macd_15_day.shape[0]):
        cur = macd_15_day.iloc[i]
        cur_time = cur['time']
        if cur['dif'] <= 0:
            dead_5 = dead_cross_5[
                (DateUtil.calculate_time(cur_time, -15) < dead_cross_5['time']) & (dead_cross_5['time'] <= cur_time)]
            if not dead_5.empty:
                __add_to_record_list(record_list, [day, dead_5.iloc[0]['time'], dead_5.iloc[0]['close'], "sell3", 100])
        else:
            if cur_time in dead_cross_soon_15['time']:
                top_5 = top_deviation_5[
                    (DateUtil.calculate_time(cur_time, -15) < top_deviation_5['time']) & (
                            top_deviation_5['time'] <= cur_time)]
                if not top_5.empty:
                    if need_load_data and \
                            macd_60_day[(DateUtil.calculate_time(cur_time, 60) > macd_60_day['time']) & (
                                    cur_time <= macd_60_day['time'])]['dif'] > 0:
                        return False
                    else:
                        __add_to_record_list(record_list,
                                             [day, top_5.iloc[0]['time'], top_5.iloc[0]['close'], "sell4", 100])
            elif cur_time in dead_cross_15['time']:
                if need_load_data and \
                        macd_60_day[(DateUtil.calculate_time(cur_time, 60) > macd_60_day['time']) & (
                                cur_time <= macd_60_day['time'])]['dif'] > 0:
                    return False
                else:
                    __add_to_record_list(record_list, [day, cur_time, cur['close'], "sell5", 100])
    return True


def day_60min_sell(day, macd_60_day, line_cross_60, line_cross_soon_60, macd_deviation_15, record_list):
    """
    60分钟即将死叉，15分钟顶背离。如果未出现15分钟顶背离，则60分钟死叉卖出。
    :param day:
    :param macd_60_day:
    :param line_cross_60:
    :param line_cross_soon_60:
    :param macd_deviation_15:
    :param record_list:
    :return:
    """
    # 正常卖出条件
    dead_cross_soon_60 = line_cross_soon_60[line_cross_soon_60['cross_soon_type'] == 'dead_soon']
    top_deviation_15 = macd_deviation_15[macd_deviation_15['deviation_type'] == 'top']
    dead_cross_60 = line_cross_60[(line_cross_60['cross_type'] == 'dead') & (line_cross_60['true_cross'] == True)]
    for i in range(macd_60_day.shape[0]):
        cur = macd_60_day.iloc[i]
        cur_time = cur['time']
        if cur_time in dead_cross_soon_60['time']:
            top_15 = top_deviation_15[
                (DateUtil.calculate_time(cur_time, -60) < top_deviation_15['time']) & (
                            top_deviation_15['time'] <= cur_time)]
            if not top_15.empty:
                __add_to_record_list(record_list, [day, top_15.iloc[0]['time'], top_15.iloc[0]['close'], "sell6", 100])
        elif cur_time in dead_cross_60['time']:
            __add_to_record_list(record_list, [day, cur_time, cur['close'], "sell7", 100])


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
