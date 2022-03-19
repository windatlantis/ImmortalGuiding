"""
K线资源接口
"""

import datetime
from abc import ABCMeta, abstractmethod
from main.utils import DateUtil


class IStockRepository(metaclass=ABCMeta):

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
        获取最近一年K线数据
        :param stock_id:
        :param n:
        :param frequency:
        :return:
        """
        now = datetime.datetime.now()
        year_ago = now + datetime.timedelta(days=n * -365)
        return self.get_stock_data_by_date(stock_id, DateUtil.format_yymmdd(year_ago), DateUtil.format_yymmdd(now), frequency)

    def get_stock_data_pass_year(self, stock_id, frequency='d'):
        """
        获取最近一年K线数据
        :param stock_id:
        :param frequency:
        :return:
        """
        return self.get_stock_data_n_year_ago(stock_id, 1, frequency)
