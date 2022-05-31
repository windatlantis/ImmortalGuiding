# -*- coding:utf-8 -*-
"""
@Time : 2022/5/14 15:58
@Author: windatlantis
@File : StrategyLib.py
"""

from main.strategy import Day15mStrategy
from main.domain import Analysiser


def call_day_15min(stock_id, is_stock=True):
    Day15mStrategy.day_15min(stock_id, is_stock)
    Analysiser.analysis_record(stock_id)
