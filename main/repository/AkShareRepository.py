# -*- coding:utf-8 -*-
"""
@Time : 2022/5/15 18:45
@Author: windatlantis
@File : AkShareRepository.py
"""
import akshare as ak
from pandas import DataFrame

from main.repository.IRepository import IStockRepository, IBondRepository
from main.repository import IRepository
from main.utils import DateUtil


class AkShareStockRepository(IStockRepository):

    def get_stock_data_by_date(self, stock_id, start_date, end_date, frequency='daily'):
        if frequency == 'd':
            frequency = 'daily'
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock_id, period=frequency,
                                                start_date=start_date.replace('-', ''),
                                                end_date=end_date.replace('-', ''), adjust='')
        return stock_zh_a_hist_df


class AkShareBondRepository(IBondRepository):

    @staticmethod
    def __data_convert(rs: DataFrame, stock_id, time='day'):
        if time == 'day':
            code_arr = [stock_id for i in range(rs.shape[0])]
            rs.insert(1, 'code', code_arr)
            rs.columns = IRepository.bond_day_fields
        else:
            temp_fields = ['date', 'open', 'high', 'low', 'close', 'volume']
            rs = rs.iloc[:, [0, 1, 2, 3, 4, 7]]
            rs.columns = temp_fields
            rs['time'] = rs['date'].apply(lambda x: DateUtil.date2time(x))
            rs['date'] = rs['date'].apply(lambda x: x.date())
            code_arr = [stock_id for i in range(rs.shape[0])]
            rs.insert(1, 'code', code_arr)
            rs = rs[[IRepository.bond_day_fields]]
        return rs

    def get_bond_data_daily(self, stock_id, start_date, end_date, frequency='d'):
        result = ak.bond_zh_hs_cov_daily(symbol=stock_id)
        return self.__data_convert(result, stock_id)

    def get_bond_data_min(self, stock_id, start_date, end_date, frequency='5'):
        result = ak.bond_zh_hs_cov_min(symbol=stock_id, period=frequency, adjust='',
                                       start_date=start_date + '09:30:00',
                                       end_date=end_date + "15:00:00")
        return self.__data_convert(result, stock_id)
