# -*- coding:utf-8 -*-
"""
@Time : 2022/3/5 10:52
@Author: windatlantis
@File : CollectionUtil.py
"""
from pandas import Series


def round2(arr):
    """
    保留两位小数
    :param arr:
    :return:
    """
    custom_values(arr, lambda x: round(float(x), 2))

    return


def custom_values(arr, func):
    """
    自定义修改序列
    :param arr:
    :param func:
    :return:
    """
    if isinstance(arr, Series):
        series = arr
        for i in range(series.size):
            series.values[i] = func(series.values[i])
    else:
        for i in range(arr.size):
            arr[i] = func(arr[i])

    return
