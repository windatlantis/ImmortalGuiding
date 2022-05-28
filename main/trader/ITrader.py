# -*- coding:utf-8 -*-
"""
@Time : 2022/5/28 15:00
@Author: windatlantis
@File : ITrader.py
"""
from abc import ABCMeta, abstractmethod


class ITrader(metaclass=ABCMeta):

    @abstractmethod
    def buy(self, stock_id, day, time, price, operation, **kwargs):
        pass

    @abstractmethod
    def sell(self, stock_id, day, time, price, operation, **kwargs):
        pass

    @abstractmethod
    def last_record(self, stock_id):
        pass