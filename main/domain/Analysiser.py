# -*- coding:utf-8 -*-
"""
@Time : 2022/5/26 0:15
@Author: windatlantis
@File : Analysiser.py
"""

from main.utils import FileUtil

record_file_name = 'record_list_{}'
analysis_file_name = 'record_list_{}_analysis'


def save_record(record_list, stock_id):
    """
    保存记录
    :param record_list:
    :param stock_id:
    :return:
    """
    FileUtil.write_csv(record_list, record_file_name.format(stock_id))
    print('save_record')


def analysis_record(stock_id):
    """
    获利分析
    :param stock_id:
    :return:
    """
    record_list = FileUtil.read_csv(record_file_name.format(stock_id))
    count = 0
    stock = 0
    earns = []
    percents = []
    for i in range(record_list.shape[0]):
        cur = record_list.iloc[i]
        earn = 0
        percent = ''
        if cur['stocks'] > 0:
            count = count + float(cur['price']) * 100
            stock = cur['stocks']
        if cur['stocks'] == 0 and not stock == 0:
            earn = float(cur['price']) * stock * 100 - count
            percent = '{0}%'.format(round(earn / count * 100, 2))
            count = 0
            stock = 0
        earns.append(earn)
        percents.append(percent)
    record_list.insert(record_list.shape[1], 'earns', earns)
    record_list.insert(record_list.shape[1], 'percents', percents)
    FileUtil.write_csv(record_list, analysis_file_name.format(stock_id))
    print('analysis_record')
