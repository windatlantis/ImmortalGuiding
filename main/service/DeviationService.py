# -*- coding:utf-8 -*-
"""
@Time : 2022/5/14 15:56
@Author: windatlantis
@File : DeviationService.py
"""

import pandas as pd
from pandas import DataFrame

from main.utils import CollectionUtil


def high_low_price(price_data: DataFrame, price_name='close', date_name='date'):
    """
    寻找价格高点,高点创30日新高,大于前一个高点
    寻找价格低点,高点创30日新低,小于前一个低点
    :param price_data:
    :param price_name:
    :param date_name:
    :return:
    """
    df_extend = pd.DataFrame(columns=[date_name, price_name, 'high_point', 'low_point'])
    line_number = int(price_data.shape[0])
    for i in range(1, line_number):
        cur = price_data.iloc[i]
        cur_price = cur[price_name]
        # 前后两根K线
        last_day_price = price_data[price_name][i - 1]
        next_day_price = cur_price if i == line_number - 1 else price_data[price_name][i + 1]
        # 30天内
        thirty_day_ago_idx = 0 if i <= 30 else i - 30
        thirty_day_max_price = price_data[price_name][thirty_day_ago_idx:i].max()
        thirty_day_min_price = price_data[price_name][thirty_day_ago_idx:i].min()
        # 前高、前低
        last_high_point = CollectionUtil.df_getlast(df_extend.loc[df_extend['high_point'] == True, price_name], 0)
        last_low_point = CollectionUtil.df_getlast(df_extend.loc[df_extend['low_point'] == True, price_name], 0)
        # 高点、低点
        high_point = cur_price > last_day_price and cur_price >= next_day_price and cur_price > thirty_day_max_price \
                     and (cur_price > last_high_point or last_high_point == 0)
        low_point = cur_price < last_day_price and cur_price <= next_day_price and cur_price < thirty_day_min_price \
                    and (cur_price < last_low_point or last_low_point == 0)
        if high_point or low_point:
            CollectionUtil.df_add(df_extend, [cur[date_name], cur_price, high_point, low_point])
    return df_extend


def collect_price_macd_deviation(macd_data: DataFrame, point_extend: DataFrame, price_name='close', date_name='date'):
    """
    获取价格macd指标背离
    :param macd_data:
    :param point_extend:
    :param price_name:
    :param date_name:
    :return:
    """
    deviation_collector = pd.DataFrame(columns=[date_name, price_name, 'macd_type', 'compare_date'])
    merge_result = pd.merge(point_extend, macd_data, on=date_name, how='left')
    high_point = merge_result.loc[merge_result['high_point'] == True]
    for i in range(1, int(high_point.shape[0])):
        cur = merge_result.iloc[i]
        last = merge_result.iloc[i - 1]
        if cur[price_name] > last[price_name] and cur['dif'] < last['dif']:
            CollectionUtil.df_add(deviation_collector, [cur[date_name], cur[price_name], '顶背离', last[date_name]])
    low_point = merge_result.loc[merge_result['low_point'] == True]
    for i in range(1, int(low_point.shape[0])):
        cur = merge_result.iloc[i]
        last = merge_result.iloc[i - 1]
        if cur[price_name] < last[price_name] and cur['dif'] > last['dif']:
            CollectionUtil.df_add(deviation_collector, [cur[date_name], cur[price_name], '底背离', last[date_name]])
    return deviation_collector


def golden_cross(macd_price_data: DataFrame, price_name='close', date_name='date'):
    """
    macd金叉
    :param macd_price_data:
    :param price_name:
    :param date_name:
    :return:
    """
    df_extend = pd.DataFrame(columns=[date_name, price_name, 'macd', 'golden_cross'])
    line_number = int(macd_price_data.shape[0])
    for i in range(1, line_number):
        cur = macd_price_data.iloc[i]
        last = macd_price_data.iloc[i - 1]
        if cur['macd'] > 0 > last['macd']:
            # 金叉
            CollectionUtil.df_add(df_extend, [cur[date_name], cur[price_name], cur['macd'], True])
        elif i >= 4 and CollectionUtil.is_sorted(macd_price_data.loc[i - 4:i - 2, 'macd'], 'desc') \
                and CollectionUtil.is_sorted(macd_price_data.loc[i - 2:i, price_name]):
            # "伪金叉": 如果有三根k线macd连续下降，如果第4根k线高于第3根，第5根高于第四根了，就认为是上涨了
            CollectionUtil.df_add(df_extend, [cur[date_name], cur[price_name], cur['macd'], False])
    return df_extend


def collect_macd_deviation(macd_data: DataFrame, cross_extend: DataFrame, price_name='close', date_name='date'):
    """
    获取macd指标背离
    :param macd_data:
    :param cross_extend:
    :param price_name:
    :param date_name:
    :return:
    """
    deviation_collector = pd.DataFrame(columns=[date_name, price_name, 'macd_type', 'compare_date'])
    # merge_result = pd.merge(cross_extend, macd_data, on=date_name, how='left')
    for i in range(1, int(cross_extend.shape[0])):
        cur = cross_extend.iloc[i]
        last = cross_extend.iloc[i - 1]
        if cur['macd'] > last['macd']:
            CollectionUtil.df_add(deviation_collector, [cur[date_name], cur[price_name], '底背离', last[date_name]])
    return deviation_collector
