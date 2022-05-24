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
    if isinstance(data, DataFrame):
        for i in range(data.shape[0]):
            table.loc[table.shape[0]] = data.iloc[i]
    else:
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


def is_sorted(table, ordered='asc') -> bool:
    """
    检查是否数据顺序
    :param table:
    :param ordered:
    :return:
    """
    if ordered == 'asc':
        # 正序
        return all([table.iloc[i + 1] > table.iloc[i] for i in range(len(table) - 1)])
    elif ordered == 'desc':
        # 倒序
        return all([table.iloc[i + 1] < table.iloc[i] for i in range(len(table) - 1)])
    return False
