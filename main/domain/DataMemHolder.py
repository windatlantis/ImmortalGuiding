# -*- coding:utf-8 -*-
"""
@Time : 2022/5/28 14:30
@Author: windatlantis
@File : DataMemHolder.py
"""
from main.domain import DataCreator
from main.utils import DateUtil

__stock_cache = {}
__bond_cache = {}


def get_stock_from_mem(stock_id):
    cache = __stock_cache.get(stock_id)
    if cache is None:
        cache = StockMemHolder(stock_id)
        __stock_cache[stock_id] = cache
    return cache


def get_bond_from_mem(stock_id):
    cache = __bond_cache.get(stock_id)
    if cache is None:
        cache = BondMemHolder(stock_id)
        __bond_cache[stock_id] = cache
    return cache


class StockMemHolder:

    def __init__(self, stock_id, read_csv=True):
        day_macd, day_macd_data = DataCreator.get_stock_n_year_macd(stock_id, 1, read_csv)
        min60_macd, min60_macd_data = DataCreator.get_stock_n_year_macd(stock_id, 1, read_csv, frequency='60')
        min15_macd, min15_macd_data = DataCreator.get_stock_n_year_macd(stock_id, 1, read_csv, frequency='15')
        min5_macd, min5_macd_data = DataCreator.get_stock_n_year_macd(stock_id, 1, read_csv, frequency='5')
        self.day_macd_data = day_macd_data
        self.min60_macd_data = min60_macd_data
        self.min15_macd_data = min15_macd_data
        self.min5_macd_data = min5_macd_data
        trade_day = []
        for i in day_macd_data['date']:
            trade_day.append(DateUtil.str2day(i))
        self.trade_date = trade_day


class BondMemHolder:

    def __init__(self, stock_id, read_csv=True):
        day_macd, day_macd_data = DataCreator.get_bond_n_month_macd(stock_id, 6, read_csv)
        min60_macd, min60_macd_data = DataCreator.get_bond_n_month_macd(stock_id, 6, read_csv, frequency='60')
        min15_macd, min15_macd_data = DataCreator.get_bond_n_month_macd(stock_id, 6, read_csv, frequency='15')
        min5_macd, min5_macd_data = DataCreator.get_bond_n_month_macd(stock_id, 6, read_csv, frequency='5')
        self.day_macd_data = day_macd_data
        self.min60_macd_data = min60_macd_data
        self.min15_macd_data = min15_macd_data
        self.min5_macd_data = min5_macd_data
        trade_day = []
        for i in day_macd_data['date']:
            trade_day.append(DateUtil.str2day(i))
        self.trade_date = trade_day
