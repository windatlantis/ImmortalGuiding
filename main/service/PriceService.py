# -*- coding:utf-8 -*-
"""
@Time : 2022/5/15 16:12
@Author: windatlantis
@File : PriceService.py
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