# -*- coding:utf-8 -*-
"""
@Time : 2022/5/15 15:35
@Author: windatlantis
@File : LineCrossService.py
"""
from pandas import DataFrame
import pandas as pd

from main.utils import CollectionUtil


def line_cross(macd_price_data: DataFrame, line_name='macd', price_name='close', date_name='date'):
    """
    金叉死叉
    :param macd_price_data:
    :param line_name:
    :param price_name:
    :param date_name:
    :return:
    """
    date_arr = ['date'] if date_name == 'date' else ['date', date_name]
    date_size = len(date_arr)
    df_extend = pd.DataFrame(columns=date_arr + [line_name, price_name, 'zero_axis', 'cross_type', 'true_cross'])
    line_number = int(macd_price_data.shape[0])
    for i in range(1, line_number):
        cur = macd_price_data.iloc[i]
        last = macd_price_data.iloc[i - 1]
        cross_type = None
        true_cross = False
        if cur[line_name] >= 0 > last[line_name]:
            # 金叉
            cross_type = 'golden'
            true_cross = True
        elif cur[line_name] <= 0 < last[line_name]:
            # 死叉
            cross_type = 'dead'
            true_cross = True
        if cross_type is None and i >= 4:
            if CollectionUtil.is_sorted(macd_price_data.loc[i - 4:i - 1, line_name], 'desc') \
                    and CollectionUtil.is_sorted(macd_price_data.loc[i - 2:i + 1, price_name]):
                # "伪金叉": 如果有三根k线macd连续下降，如果第4根k线高于第3根，第5根高于第四根了，就认为是上涨了
                cross_type = 'golden'
            elif CollectionUtil.is_sorted(macd_price_data.loc[i - 4:i - 1, line_name]) \
                    and CollectionUtil.is_sorted(macd_price_data.loc[i - 2:i + 1, price_name], 'desc'):
                # "伪死叉": 如果有三根k线macd连续上升，如果第4根k线低于第3根，第5根低于第四根了，就认为是伪死叉
                cross_type = 'dead'
        if cross_type is not None:
            data = [cur[date_name], cur[line_name], cur[price_name], cur['dif'], cross_type, true_cross]
            if date_size == 2:
                data.insert(0, cur['date'])
            CollectionUtil.df_add(df_extend, data)
    return df_extend


def line_cross_soon(macd_price_data: DataFrame, line_name='macd', price_name='close', date_name='date'):
    """
    即将金叉死叉
    :param macd_price_data:
    :param line_name:
    :param price_name:
    :param date_name:
    :return:
    """
    date_arr = ['date'] if date_name == 'date' else ['date', date_name]
    date_size = len(date_arr)
    df_extend = pd.DataFrame(columns=date_arr + [line_name, price_name, 'zero_axis', 'cross_soon_type'])
    line_number = int(macd_price_data.shape[0])
    for i in range(2, line_number):
        cur = macd_price_data.iloc[i]
        cross_type = None
        if -0.05 < cur[line_name] < 0 and CollectionUtil.is_sorted(macd_price_data.loc[i - 2:i + 1, line_name]):
            # 即将金叉:MACD连续三根上涨，并且上涨至-0.05以内
            cross_type = 'golden_soon'
        elif cur[line_name] > 0 and CollectionUtil.is_sorted(macd_price_data.loc[i - 2:i + 1, line_name], 'desc'):
            # 即将死叉:MACD连续三根下跌(MACD值是正的)
            cross_type = 'dead_soon'
        if cross_type is not None:
            data = [cur[date_name], cur[line_name], cur[price_name], cur['dif'], cross_type]
            if date_size == 2:
                data.insert(0, cur['date'])
            CollectionUtil.df_add(df_extend, data)
    return df_extend


def filter_dead_cross(line_cross_: DataFrame, is_true=True):
    if is_true:
        return line_cross_[(line_cross_['cross_type'] == 'dead') & (line_cross_['true_cross'] == True)]
    return line_cross_[(line_cross_['cross_type'] == 'dead')]


def filter_golden_cross(line_cross_: DataFrame, is_true=True):
    if is_true:
        return line_cross_[(line_cross_['cross_type'] == 'golden') & (line_cross_['true_cross'] == True)]
    return line_cross_[(line_cross_['cross_type'] == 'golden')]


def filter_dead_cross_soon(line_cross_: DataFrame):
    return line_cross_[(line_cross_['cross_soon_type'] == 'dead_soon')]


def filter_golden_cross_soon(line_cross_: DataFrame):
    return line_cross_[(line_cross_['cross_soon_type'] == 'golden_soon')]
