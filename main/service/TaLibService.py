# -*- coding:utf-8 -*-
"""
@Time : 2022/3/5 11:17
@Author: windatlantis
@File : TaLibService.py
"""

import talib as ta


def get_macd(close):
    macdDIF, macdDEA, macd = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    macd = macd * 2
    return macdDIF, macdDEA, macd
