# -*- coding:utf-8 -*-
"""
@Time : 2022/5/2 23:00
@Author: windatlantis
@File : FileUtil.py
"""
import os

import datetime
from pandas import DataFrame
import pandas as pd

from main.utils import DateUtil

csv_path = 'd:/{}.csv'


def write_csv(data: DataFrame, name='', index=True):
    """
    写csv文件
    :param data:
    :param name:
    :param index:
    :return:
    """
    if name == '':
        name = DateUtil.format_yymmdd_hhmmss_long(datetime.datetime.now())
    data.to_csv(csv_path.format(name), index=index)


def read_csv(name):
    """
    读csv文件
    :param name:
    :return:
    """
    path = csv_path.format(name)
    data = None
    if os.path.exists(path):
        data = pd.read_csv(path)
    return data


def exist_csv(name):
    """
    判断csv文件是否存在
    :param name:
    :return:
    """
    path = csv_path.format(name)
    return os.path.exists(path)
