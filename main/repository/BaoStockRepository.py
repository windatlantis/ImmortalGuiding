# -*- coding:utf-8 -*-
"""
baostock相关资源
@Time : 2022/2/26 11:26
@Author: windatlantis
@File : BaoStockRepository.py
"""

from main.repository.IRepository import IStockRepository
from main.repository import RepoConstants
import baostock as bs
import pandas as pd


class BaoStockRepository(IStockRepository):

    def __login(self):
        #### 登陆系统 ####
        lg = bs.login()
        # 显示登陆返回信息
        print('login respond error_code:' + lg.error_code)
        print('login respond error_msg:' + lg.error_msg)

    def __logout(self):
        #### 登出系统 ####
        bs.logout()

    def __convert_to_pandas(self, rs):
        #### 结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        return result

    def get_stock_data_by_date(self, stock_id, start_date, end_date, frequency='d', adjustflag="3"):
        self.__login()

        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus(stock_id,
                                          RepoConstants.fields,
                                          start_date, end_date,
                                          frequency, adjustflag)
        print('query_history_k_data_plus respond error_code:' + rs.error_code)
        print('query_history_k_data_plus respond error_msg:' + rs.error_msg)

        self.__logout()

        return self.__convert_to_pandas(rs)
