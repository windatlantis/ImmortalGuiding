# -*- coding:utf-8 -*-
"""
@Time : 2022/5/15 18:45
@Author: windatlantis
@File : AkShareRepository.py
"""
import akshare as ak
from pandas import DataFrame

from main.repository.IRepository import IStockRepository, IBondRepository
from main.repository import IRepository, RepoConstants
from main.utils import DateUtil

frequency_mapping = {'d': 'daily', 'w': 'weekly', 'm': 'monthly'}


def data_convert(rs: DataFrame, stock_id, time='daily'):
    if time in RepoConstants.ak_frequency or time in RepoConstants.bao_frequency:
        code_arr = [stock_id for i in range(rs.shape[0])]
        rs.insert(1, 'code', code_arr)
    else:
        temp_fields = ['date', 'open', 'close', 'high', 'low', 'volume']
        rs = rs.iloc[:, [0, 1, 2, 3, 4, 7]]
        rs.columns = temp_fields
        copy = rs.copy()
        copy['time'] = copy['date'].apply(lambda x: DateUtil.date2time(DateUtil.str2day(x, DateUtil.yymmdd_hhmmss)))
        copy['date'] = copy['date'].apply(lambda x: DateUtil.str2day(x, DateUtil.yymmdd_hhmmss).date())
        code_arr = [stock_id for i in range(rs.shape[0])]
        copy.insert(1, 'code', code_arr)
        copy = copy[IRepository.bond_min_fields]
        rs = copy.copy()
    return rs


class AkShareStockRepository(IStockRepository):

    def get_stock_data_by_date(self, stock_id, start_date, end_date, frequency='daily'):
        if frequency in RepoConstants.bao_frequency:
            frequency = frequency_mapping.get(frequency)
        if frequency in RepoConstants.ak_frequency:
            result = ak.stock_zh_a_hist(symbol=stock_id, period=frequency,
                                        start_date=start_date.replace('-', ''),
                                        end_date=end_date.replace('-', ''), adjust='')
        else:
            result = ak.stock_zh_a_hist_min_em(symbol=stock_id, period=frequency, adjust='',
                                               start_date=start_date + ' 09:30:00',
                                               end_date=end_date + " 15:00:00")
        return data_convert(result, stock_id, frequency)


class AkShareBondRepository(IBondRepository):

    def get_bond_data_daily(self, stock_id, start_date, end_date, frequency='d'):
        result = ak.bond_zh_hs_cov_daily(symbol=stock_id.replace('.', ''))
        return data_convert(result, stock_id, frequency)

    def get_bond_data_min(self, stock_id, start_date, end_date, frequency='5'):
        result = ak.bond_zh_hs_cov_min(symbol=stock_id.replace('.', ''), period=frequency, adjust='',
                                       start_date=start_date + ' 09:30:00',
                                       end_date=end_date + " 15:00:00")
        return data_convert(result, stock_id, frequency)
