# -*- coding:utf-8 -*-
"""
@Time : 2022/5/14 15:56
@Author: windatlantis
@File : DeviationService.py
"""

import pandas as pd
from pandas import DataFrame

from main.utils import CollectionUtil


def collect_price_macd_deviation(macd_data: DataFrame, point_extend: DataFrame, price_name='close', date_name='date'):
    """
    获取价格macd指标背离
    顶背离：股价创出新高，但是指标没有新高，反而呈下降趋势
    底背离：股价创出新低，但是指标没有新低，反而呈上升趋势
    :param macd_data:
    :param point_extend:
    :param price_name:
    :param date_name:
    :return:
    """
    deviation_collector = pd.DataFrame(columns=[date_name, price_name, 'deviation_type', 'compare_date'])
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


def collect_macd_deviation(cross_extend: DataFrame, price_name='close', date_name='date'):
    """
    单macd指标背离
    底背离：2个macd金叉点，下一个比上一个高
    顶背离：2个macd死叉点，下一个比上一个低
    :param cross_extend: 
    :param price_name: 
    :param date_name: 
    :return: 
    """
    deviation_collector = pd.DataFrame(columns=[date_name, price_name, 'zero_axis', 'deviation_type', 'compare_date'])
    for i in range(1, int(cross_extend.shape[0])):
        cur = cross_extend.iloc[i]
        last = cross_extend.iloc[i - 1]
        if cur['macd'] > last['macd']:
            CollectionUtil.df_add(deviation_collector, [cur[date_name], cur[price_name], cur['zero_axis'], 'bottom', last[date_name]])
        elif cur['macd'] < last['macd']:
            CollectionUtil.df_add(deviation_collector, [cur[date_name], cur[price_name], cur['zero_axis'], 'top', last[date_name]])
    return deviation_collector
