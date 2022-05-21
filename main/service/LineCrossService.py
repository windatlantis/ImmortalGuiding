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
    df_extend = pd.DataFrame(columns=[date_name, line_name, price_name, 'zero_axis', 'cross_type', 'true_cross'])
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
        else:
            if i >= 2:
                if -0.05 < cur[line_name] < 0 and CollectionUtil.is_sorted(macd_price_data.loc[i - 2:i, line_name]):
                    # 即将金叉:MACD连续三根上涨，并且上涨至-0.05以内
                    cross_type = 'golden_soon'
                elif cur[line_name] > 0 and CollectionUtil.is_sorted(macd_price_data.loc[i - 2:i, line_name], 'desc'):
                    # 即将死叉:MACD连续三根下跌(MACD值是正的)
                    cross_type = 'dead_soon'
            if i >= 4:
                if CollectionUtil.is_sorted(macd_price_data.loc[i - 4:i - 2, line_name],
                                            'desc') and CollectionUtil.is_sorted(
                    macd_price_data.loc[i - 2:i, price_name]):
                    # "伪金叉": 如果有三根k线macd连续下降，如果第4根k线高于第3根，第5根高于第四根了，就认为是上涨了
                    cross_type = 'golden'
                elif CollectionUtil.is_sorted(macd_price_data.loc[i - 4:i - 2, line_name]) and CollectionUtil.is_sorted(
                        macd_price_data.loc[i - 2:i, price_name], 'desc'):
                    # "伪死叉": 如果有三根k线macd连续上升，如果第4根k线低于第3根，第5根低于第四根了，就认为是伪死叉
                    cross_type = 'dead'

        if cross_type is not None:
            CollectionUtil.df_add(df_extend,
                                  [cur[date_name], cur[line_name], cur[price_name], cur['dif'], cross_type, true_cross])
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
    df_extend = pd.DataFrame(columns=[date_name, line_name, price_name, 'zero_axis', 'cross_soon_type'])
    line_number = int(macd_price_data.shape[0])
    for i in range(2, line_number):
        cur = macd_price_data.iloc[i]
        cross_soon_type = None
        if -0.05 < cur[line_name] < 0 and CollectionUtil.is_sorted(macd_price_data.loc[i - 2:i, line_name]):
            # 即将金叉:MACD连续三根上涨，并且上涨至-0.05以内
            cross_soon_type = 'golden'
        elif 0 < cur[line_name] < 0.05 and CollectionUtil.is_sorted(macd_price_data.loc[i - 2:i, line_name], 'desc'):
            # 即将死叉:MACD连续三根下跌，并且下跌至0.05以内
            cross_soon_type = 'dead'

        if cross_soon_type is not None:
            CollectionUtil.df_add(df_extend,
                                  [cur[date_name], cur[line_name], cur[price_name], cur['dif'], cross_soon_type])
    return df_extend
