# -*- coding:utf-8 -*-
"""
@Time : 2022/5/15 18:45
@Author: windatlantis
@File : AkShareRepository.py
"""
import akshare as ak

from main.repository.IRepository import IStockRepository


class AkShareRepository(IStockRepository):

    def get_stock_data_by_date(self, stock_id, start_date, end_date, frequency='daily'):
        if frequency == 'd':
            frequency = 'daily'
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock_id, period=frequency,
                                                start_date=start_date.replace('-', ''),
                                                end_date=end_date.replace('-', ''), adjust="qfq")
        return stock_zh_a_hist_df
