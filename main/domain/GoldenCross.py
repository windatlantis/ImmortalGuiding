# -*- coding:utf-8 -*-
"""
@Time : 2022/3/5 10:43
@Author: windatlantis
@File : GoldenCross.py
"""
from main.repository.BaoStockRepository import BaoStockRepository
from main.service import TaLibService, MatplotService
from main.utils import SeriesUtil
import pandas as pd


def draw_macd_pic():
    bao = BaoStockRepository()
    result = bao.get_stock_data_pass_year('sh.601398')
    result.to_csv('d:/600036.csv')
    MatplotService.init_plt_style()

    SeriesUtil.round2(result['close'])
    close = result['close']

    macdDIF, macdDEA, macd = TaLibService.get_macd(close)

    df_macd = pd.DataFrame([macdDIF, macdDEA, macd], index=['dif', 'dea', 'macd'])
    df_macd = df_macd.T
    df_macd.to_csv('d:/600036_macd.csv')

    MatplotService.show(df_macd, '招商银行近一年macd', '时间')
