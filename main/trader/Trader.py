# -*- coding:utf-8 -*-
"""
@Time : 2022/5/28 13:59
@Author: windatlantis
@File : Trader.py
"""

from main.trader.ITrader import ITrader
import pandas as pd

from main.utils import CollectionUtil


class Trader(ITrader):

    def __init__(self):
        self.record_map = {}

    def buy(self, stock_id, day, time, price, operation, **kwargs):
        record_list = self.record_map.get(stock_id)
        if record_list is None:
            record_list = pd.DataFrame(columns=['date', 'time', 'price', 'operation', 'zero_axis_60'])
            self.record_map[stock_id] = record_list
        last_one = CollectionUtil.df_getlast(record_list, None)
        if 'buy1' == operation and last_one is not None and 'buy2' == last_one:
            print(f'{operation} is repeat, time {time}')
            return
        CollectionUtil.df_add(record_list, [day, time, price, operation, kwargs.get('zero_axis_60')])

    def sell(self, stock_id, day, time, price, operation, **kwargs):
        record_list = self.record_map.get(stock_id)
        if record_list is None:
            record_list = pd.DataFrame(columns=['date', 'time', 'price', 'operation', 'zero_axis_60'])
            self.record_map[stock_id] = record_list
        CollectionUtil.df_add(record_list, [day, time, price, operation, kwargs.get('zero_axis_60')])

    def last_record(self, stock_id):
        record_list = self.record_map.get(stock_id)
        if record_list is None:
            return None
        return CollectionUtil.df_getlast(record_list, None)
