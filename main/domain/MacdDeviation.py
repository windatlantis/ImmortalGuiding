# -*- coding:utf-8 -*-
"""
@Time : 2022/5/14 21:22
@Author: windatlantis
@File : MacdDeviation.py
"""
from main.domain import DataCreator
from main.service import DeviationService


def print_deviation(stock_id, read_csv=True):
    df_macd, df_macd_data = DataCreator.get_n_year_macd(stock_id, 1, read_csv)
    # high_low_price = DeviationService.high_low_price(df_macd_data)
    # print(high_low_price)
    # deviations = DeviationService.collect_price_macd_deviation(df_macd_data, high_low_price)
    # print(deviations)
    # golden_cross = DeviationService.golden_cross(df_macd_data)
    # print(golden_cross)
    # deviations = DeviationService.collect_macd_deviation(df_macd_data, golden_cross)
    # print(deviations)