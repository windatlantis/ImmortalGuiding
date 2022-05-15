# -*- coding:utf-8 -*-
"""
@Time : 2022/5/2 18:03
@Author: windatlantis
@File : DataCreator.py
"""
import pandas as pd

from main.repository import RepoConstants
from main.repository.BaoStockRepository import BaoStockRepository
from main.service import TaLibService
from main.utils import CollectionUtil
from main.utils import FileUtil


def get_n_year_macd(stock_id, year, read_csv=True, frequency='d'):
    """
    获取macd
    :param stock_id:
    :param year:
    :param read_csv:
    :param frequency:
    :return:
    """
    macd_file = '{}_{}_{}y_macd'.format(stock_id, frequency, year)
    macd_data_file = '{}_{}_{}y_macd_data'.format(stock_id, frequency, year)
    if read_csv and FileUtil.exist_csv(macd_file) and FileUtil.exist_csv(macd_data_file):
        macd_result = FileUtil.read_csv(macd_file)
        macd_data_result = FileUtil.read_csv(macd_data_file)
        return macd_result, macd_data_result

    bao = BaoStockRepository()
    # k线数据
    result = bao.get_stock_data_n_year_ago(stock_id, year, frequency)

    # 获取3条线的数据
    macdDIF, macdDEA, macd = TaLibService.get_macd(result['close'].astype(float).values)
    # 小数点后两位
    CollectionUtil.round2(macdDIF)
    CollectionUtil.round2(macdDEA)
    CollectionUtil.round2(macd)

    date_name = 'date'
    if frequency in RepoConstants.frequency_min:
        date_name = 'time'
    # 前33个为Nan，所以推荐用于计算的数据量一般为你所求日期之间数据量的3倍
    df_macd = pd.DataFrame({"dif": macdDIF[33:], "dea": macdDEA[33:], "macd": macd[33:]}, index=result[date_name][33:],
                           columns=['dif', 'dea', 'macd'])
    # 与原数据合并
    df_macd_data = pd.merge(df_macd, result, on=date_name, how='left')

    # 写文件
    if read_csv:
        FileUtil.write_csv(result, '{}_{}_{}y_close'.format(stock_id, frequency, year))
        FileUtil.write_csv(df_macd, macd_file)
        FileUtil.write_csv(df_macd_data, macd_data_file, index=False)
    return df_macd, df_macd_data


def get_one_year_macd(stock_id, read_csv=True, frequency='d'):
    """
    获取macd
    :param stock_id:
    :param read_csv:
    :param frequency:
    :return:
    """
    return get_n_year_macd(stock_id, 1, read_csv, frequency)
