"""
K线资源接口
"""

import datetime
from abc import ABCMeta, abstractmethod
from main.utils import DateUtil
from main.repository import RepoConstants

stock_day_fields = ['date', 'code', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount']
stock_min_fields = ['date', 'time', 'code', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount']

bond_day_fields = ['date', 'code', 'open', 'high', 'low', 'close', 'volume']
bond_min_fields = ['date', 'time', 'code', 'open', 'high', 'low', 'close', 'volume']


class IStockRepository(metaclass=ABCMeta):
    """
    股票接口
    """

    @abstractmethod
    def get_stock_data_by_date(self, stock_id, start_date, end_date, frequency='d'):
        """
        按照时间获取K线数据
        :param stock_id:
        :param start_date:
        :param end_date:
        :param frequency:
        :return:
        """
        pass

    def get_stock_data_n_year_ago(self, stock_id, n, frequency='d'):
        """
        获取最近n年K线数据
        :param stock_id:
        :param n:
        :param frequency:
        :return:
        """
        now = datetime.datetime.today()
        year_ago = now + datetime.timedelta(days=n * -365)
        return self.get_stock_data_by_date(stock_id, DateUtil.format_yymmdd(year_ago), DateUtil.format_yymmdd(now),
                                           frequency)

    def get_stock_data_pass_year(self, stock_id, frequency='d'):
        """
        获取最近一年K线数据
        :param stock_id:
        :param frequency:
        :return:
        """
        return self.get_stock_data_n_year_ago(stock_id, 1, frequency)

    def get_stock_data_n_month_age(self, stock_id, n, frequency='d'):
        """
        获取最近n月K线数据
        :param stock_id:
        :param n:
        :param frequency:
        :return:
        """
        now = datetime.datetime.today()
        month_ago = now + datetime.timedelta(days=n * -30)
        return self.get_stock_data_by_date(stock_id, DateUtil.format_yymmdd(month_ago), DateUtil.format_yymmdd(now),
                                           frequency)


class IBondRepository(metaclass=ABCMeta):
    """
    转债接口
    """

    @abstractmethod
    def get_bond_data_daily(self, stock_id, start_date, end_date, frequency='d'):
        """
        按照时间获取K线数据，日线
        :param stock_id:
        :param start_date:
        :param end_date:
        :param frequency:
        :return:
        """
        pass

    @abstractmethod
    def get_bond_data_min(self, stock_id, start_date, end_date, frequency='5'):
        """
        按照时间获取K线数据，分钟级别
        :param stock_id:
        :param start_date:
        :param end_date:
        :param frequency:
        :return:
        """
        pass

    def get_bond_data_by_date(self, stock_id, start_date, end_date, frequency='d'):
        if frequency in RepoConstants.bao_frequency:
            return self.get_bond_data_daily(stock_id, start_date, end_date, frequency)
        else:
            return self.get_bond_data_min(stock_id, start_date, end_date, frequency)

    def get_bond_data_n_month_ago(self, stock_id, n, frequency='d'):
        now = datetime.datetime.today()
        month_ago = now + datetime.timedelta(days=n * -30)
        return self.get_bond_data_by_date(stock_id, DateUtil.format_yymmdd(month_ago), DateUtil.format_yymmdd(now),
                                          frequency)
