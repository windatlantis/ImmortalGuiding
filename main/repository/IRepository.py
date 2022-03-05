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

    def get_stock_data_pass_year(self, stock_id, frequency='d'):
        """
        获取最近一年K线数据
        :param stock_id:
        :param frequency:
        :return:
        """
        now = datetime.datetime.now()
        year_ago = now + datetime.timedelta(days=-365)
        return self.get_stock_data_by_date(stock_id, start_date=DateUtil.format_yymmdd(year_ago), end_date=DateUtil.format_yymmdd(now), frequency=frequency)
