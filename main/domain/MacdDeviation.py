# -*- coding:utf-8 -*-
"""
@Time : 2022/5/14 21:22
@Author: windatlantis
@File : MacdDeviation.py
"""
from main.domain import DataCreator
from main.service import DeviationService


def print_deviation(stock_id, read_csv=True):
    df_macd, df_macd_data = DataCreator.get_one_year_macd(stock_id, read_csv)
    high_low_price = DeviationService.high_low_price(df_macd_data)
    deviations = DeviationService.collect_deviation(df_macd, high_low_price)
    print(deviations)