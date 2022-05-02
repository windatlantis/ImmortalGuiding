# -*- coding:utf-8 -*-
"""
@Time : 2022/3/5 10:43
@Author: windatlantis
@File : GoldenCross.py
"""

import pandas as pd
from pandas import DataFrame

from main.service import MatplotService
from main.domain import DataCreator
from main.utils import FileUtil


def print_cross_useful(stock_id, read_csv=True):
    """
    打印金叉、死叉
    :param stock_id:
    :param read_csv:
    :return:
    """
    df_macd, df_macd_data = DataCreator.get_macd(stock_id, read_csv)
    # draw_macd_pic(df_macd, stock_id)
    print_cross(df_macd_data, stock_id)


def draw_macd_pic(df_macd, stock_id):
    """
    绘制macd图
    :param df_macd:
    :param stock_id:
    :return:
    """
    MatplotService.init_plt_style()
    # 绘制图片
    MatplotService.show(df_macd, title=stock_id + '近一年macd', xlabel='时间', legends=['dif', 'dea', 'macd'])


def add_high_low_point(df_macd_data):
    """
    标记价格高点、低点
    高点（收盘价高于前后两根K线,高于过去30日任何一天的收盘价）
    低点（收盘价低于前后两根K线,低于过去30日任何一天的收盘价）
    :param df_macd_data:
    :return:
    """
    df_macd_data_extend = pd.DataFrame(columns=['date', 'high_point', 'low_point'])
    line_number = int(df_macd_data.shape[0])
    for i in range(line_number):
        cur = df_macd_data.iloc[i]
        cur_close = cur['close']
        last_day_close = cur_close if i == 0 else df_macd_data['close'][i - 1]
        next_day_close = cur_close if i == line_number - 1 else df_macd_data['close'][i + 1]
        # 30天内
        thirty_day_ago_idx = 0 if i <= 30 else i - 30
        thirty_day_max_close = df_macd_data['close'][thirty_day_ago_idx:i].max()
        thirty_day_min_close = df_macd_data['close'][thirty_day_ago_idx:i].min()
        # 高点、低点
        high_point = cur_close > last_day_close and cur_close >= next_day_close and cur_close > thirty_day_max_close
        low_point = cur_close < last_day_close and cur_close <= next_day_close and cur_close < thirty_day_min_close
        df_macd_data_extend.loc[i] = {'date': cur['date'], 'high_point': high_point, 'low_point': low_point}

    merge_result = pd.merge(df_macd_data, df_macd_data_extend, on='date', how='left')
    return merge_result


def print_cross(df_macd_data, stock_id):
    """
    打印交叉数据及背离数据
    :param df_macd_data:
    :return:
    """
    df_macd_data = add_high_low_point(df_macd_data)
    FileUtil.write_csv(df_macd_data, stock_id + '_point')
    print(get_beili(df_macd_data))


def get_beili(data: DataFrame):
    """
    获取背离
    顶背离（高点价格高于前一高点，但是dif低于前一个高点）
    底背离（高点价格低于前一低点，但是dif高于前一个高点）
    :param data:
    :return:
    """
    beili_collector = pd.DataFrame(columns=['date', 'close', 'macd_type', 'compare_date'])
    line = int(data.shape[0])
    # 前高,前低
    last_high_close = pd.DataFrame(columns=['date', 'close'])
    last_low_close = pd.DataFrame(columns=['date', 'close'])
    last_high_dif = pd.DataFrame(columns=['date', 'dif'])
    last_low_dif = pd.DataFrame(columns=['date', 'dif'])
    for i in range(line):
        cur = data.iloc[i]
        cur_date = cur['date']
        cur_close = cur['close']
        cur_dif = cur['dif']
        macd_type = None
        compare_date = None

        if cur['high_point']:
            if (not last_high_close.empty) and cur_close > last_high_close.iloc[-1]['close'] and cur_dif < last_high_dif.iloc[-1]['dif']:
                macd_type = '顶背离'
                compare_date = last_high_close.iloc[-1]['date']
            last_high_close.loc[last_high_close.shape[0]] = [cur_date, cur_close]
            last_high_dif.loc[last_high_dif.shape[0]] = [cur_date, cur_dif]
        elif cur['low_point']:
            if (not last_low_close.empty) and cur_close < last_low_close.iloc[-1]['close'] and cur_dif > last_low_dif.iloc[-1]['dif']:
                macd_type = '底背离'
                compare_date = last_low_close.iloc[-1]['date']
            last_low_close.loc[last_low_close.shape[0]] = [cur_date, cur_close]
            last_low_dif.loc[last_low_dif.shape[0]] = [cur_date, cur_dif]

        if macd_type is not None:
            beili_collector.loc[beili_collector.shape[0]] = {'date': cur['date'], 'close': cur_close,
                                                             'macd_type': macd_type, 'compare_date':compare_date}

    return beili_collector
