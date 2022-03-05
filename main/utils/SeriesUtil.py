# -*- coding:utf-8 -*-
"""
@Time : 2022/3/5 10:52
@Author: windatlantis
@File : SeriesUtil.py
"""
from pandas import Series


def round2(series: Series):
    """
    保留两位小数
    :param series:
    :return:
    """
    custom_series_values(series, lambda x: round(float(x), 2))

    return


def custom_series_values(series: Series, func):
    """
    自定义修改序列
    :param series:
    :param func:
    :return:
    """
    for i in range(series.size):
        series.values[i] = func(series.values[i])

    return
