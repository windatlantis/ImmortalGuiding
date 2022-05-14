# -*- coding:utf-8 -*-
"""
@Time : 2022/3/5 10:52
@Author: windatlantis
@File : CollectionUtil.py
"""
from pandas import Series, DataFrame


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


def df_add(table: DataFrame, data):
    """
    在最后一行添加数据
    :param table:
    :param data:
    :return:
    """
    table.loc[table.shape[0]] = data


def df_getlast(table: DataFrame, or_default):
    """
    获取最后一行数据
    :param table:
    :param or_default:
    :return:
    """
    if table.empty:
        return or_default
    return table.iloc[-1]
