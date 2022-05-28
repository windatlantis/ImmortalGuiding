# -*- coding:utf-8 -*-
"""
@Time : 2022/5/28 14:07
@Author: windatlantis
@File : IStrategy.py
"""

from abc import ABCMeta, abstractmethod
from main.trader.ITrader import ITrader


class ITradeStrategy(metaclass=ABCMeta):

    @abstractmethod
    def load_data(self, stock_id, day):
        pass;

    @abstractmethod
    def load_trader(self, trader: ITrader):
        pass

    @abstractmethod
    def match(self, day, time):
        pass;
