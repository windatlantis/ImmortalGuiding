# -*- coding:utf-8 -*-
"""
@Time : 2022/5/14 15:58
@Author: windatlantis
@File : StrategyLib.py
"""

from main.strategy import Day15mStrategy


def call_day_15min(stock_id, read_csv=True):
    Day15mStrategy.day_15min_golden_cross(stock_id, read_csv)
