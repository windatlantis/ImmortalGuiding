# -*- coding:utf-8 -*-
"""
@Time : 2022/5/26 0:15
@Author: windatlantis
@File : Analysiser.py
"""

import pandas as pd
from main.utils import FileUtil, CollectionUtil, DateUtil
from datetime import datetime

record_file_name = 'record_list_{}'
analysis_file_name = 'record_list_{}_analysis'

temp_dir = ''


def save_record(record_list, stock_id):
    """
    保存记录
    :param record_list:
    :param stock_id:
    :return:
    """
    if record_list is not None:
        global temp_dir
        if temp_dir == '':
            temp_dir = DateUtil.format_yymmdd_hhmmss_long(datetime.now())
        FileUtil.write_csv_temp_dir(record_list, temp_dir, record_file_name.format(stock_id))
        print('save_record')


def analysis_record(stock_ids):
    """
    获利分析
    :param stock_ids:
    :return:
    """
    if isinstance(stock_ids, str):
        stock_ids = [stock_ids]
    total = pd.DataFrame(
        columns=['code', 'buy_date', 'buy_time', 'sell_date', 'sell_time', 'buy_price', 'sell_price',
                 'buy_type', 'sell_type', '100*earn', 'percent'])
    global temp_dir
    for stock_id in stock_ids:
        record_list = FileUtil.read_csv_temp_dir(temp_dir, record_file_name.format(stock_id))
        if record_list is None:
            print(stock_id + ' file is none')
            continue
        for i in range(1, record_list.shape[0]):
            cur = record_list.iloc[i]
            last = record_list.iloc[i - 1]
            if cur['stocks'] == 0 and last['stocks'] > 0:
                CollectionUtil.df_add(total, [stock_id, last['date'], last['time'], cur['date'], cur['time'],
                                              last['price'], cur['price'], last['operation'], cur['operation'],
                                              (cur['price'] - last['price']) * 100,
                                              '{0}%'.format(
                                                  round((cur['price'] - last['price']) / last['price'] * 100, 2))])
    FileUtil.write_csv_temp_dir(total, temp_dir, analysis_file_name.format(datetime.today().date()))
    temp_dir = ''
    print('analysis_record')


def analysis_record_only(path, stock_ids):
    """
    获利分析
    :param path:
    :param stock_ids:
    :return:
    """
    if isinstance(stock_ids, str):
        stock_ids = [stock_ids]
    total = pd.DataFrame(
        columns=['code', 'buy_date', 'buy_time', 'sell_date', 'sell_time', 'buy_price', 'sell_price',
                 'buy_type', 'sell_type', '100*earn', 'percent'])
    for stock_id in stock_ids:
        record_list = FileUtil.read_csv_temp_dir(path, record_file_name.format(stock_id))
        if record_list is None:
            print(stock_id + ' file is none')
            continue
        for i in range(1, record_list.shape[0]):
            cur = record_list.iloc[i]
            last = record_list.iloc[i - 1]
            if cur['stocks'] == 0 and last['stocks'] > 0:
                CollectionUtil.df_add(total, [stock_id, last['date'], last['time'], cur['date'], cur['time'],
                                              last['price'], cur['price'], last['operation'], cur['operation'],
                                              (cur['price'] - last['price']) * 100,
                                              '{0}%'.format(
                                                  round((cur['price'] - last['price']) / last['price'] * 100, 2))])
    FileUtil.write_csv_temp_dir(total, path, analysis_file_name.format(datetime.today().date()))
    print('analysis_record')