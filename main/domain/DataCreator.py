# -*- coding:utf-8 -*-
"""
@Time : 2022/5/2 18:03
@Author: windatlantis
@File : DataCreator.py
"""
import datetime

import pandas as pd

from main.repository import RepoConstants
from main.repository.AkShareRepository import AkShareStockRepository, AkShareBondRepository
from main.repository.BaoStockRepository import BaoStockRepository
from main.service import TaLibService
from main.utils import CollectionUtil, DateUtil
from main.utils import FileUtil

stock_repository_factory = {
    'bao': BaoStockRepository(),
    'ak': AkShareStockRepository()
}

bond_repository_factory = {
    'ak': AkShareBondRepository()
}

stock_year_file_close = '{}_{}_{}y_close'
stock_year_file_macd = '{}_{}_{}y_macd'
stock_year_file_macd_data = '{}_{}_{}y_macd_data'
stock_month_file_close = '{}_{}_{}m_close'
stock_month_file_macd = '{}_{}_{}m_macd'
stock_month_file_macd_data = '{}_{}_{}m_macd_data'
bond_month_file_close = 'b_{}_{}_{}m_close'
bond_month_file_macd = 'b_{}_{}_{}m_macd'
bond_month_file_macd_data = 'b_{}_{}_{}m_macd_data'


def __get_data(result, frequency):
    # 获取3条线的数据
    macdDIF, macdDEA, macd = TaLibService.get_macd(result['close'].astype(float).values)
    # 小数点后两位
    CollectionUtil.round_n(macdDIF, 4)
    CollectionUtil.round_n(macdDEA, 4)
    CollectionUtil.round_n(macd, 4)

    date_name = 'date'
    if frequency in RepoConstants.bao_frequency_min:
        date_name = 'time'
    # 前33个为Nan，所以推荐用于计算的数据量一般为你所求日期之间数据量的3倍
    df_macd = pd.DataFrame({"dif": macdDIF[33:], "dea": macdDEA[33:], "macd": macd[33:]}, index=result[date_name][33:],
                           columns=['dif', 'dea', 'macd'])
    # 与原数据合并
    df_macd_data = pd.merge(df_macd, result, on=date_name, how='left')
    if frequency in RepoConstants.bao_frequency_min:
        df_macd_data['time'] = df_macd_data['time'].astype(float)
    return df_macd, df_macd_data


def get_stock_n_year_macd(stock_id, year, read_csv=True, frequency='d', source='bao'):
    """
    获取macd
    :param stock_id:
    :param year:
    :param read_csv:
    :param frequency:
    :param source:
    :return:
    """
    macd_file = stock_year_file_macd.format(stock_id, frequency, year)
    macd_data_file = stock_year_file_macd_data.format(stock_id, frequency, year)
    if read_csv and FileUtil.exist_csv(macd_file) and FileUtil.exist_csv(macd_data_file):
        macd_result = FileUtil.read_csv(macd_file)
        macd_data_result = FileUtil.read_csv(macd_data_file)
        print('read_csv success')
        return macd_result, macd_data_result

    repository = stock_repository_factory.get(source)
    # k线数据
    today = datetime.datetime.today()
    result = None
    for i in range(year * 2, 0, -1):
        start = today + datetime.timedelta(days=-30 * 6 * i)
        end = start + datetime.timedelta(days=30 * 6 - 1)
        if i == 1:
            end = start + datetime.timedelta(days=30 * 6)
        data = repository.get_stock_data_by_date(stock_id, DateUtil.format_yymmdd(start),
                                                 DateUtil.format_yymmdd(end), frequency)
        if result is None:
            result = pd.DataFrame(columns=data.columns)
        CollectionUtil.df_add(result, data)

    df_macd, df_macd_data = __get_data(result, frequency)

    # 写文件
    if read_csv:
        FileUtil.write_csv(result, stock_year_file_close.format(stock_id, frequency, year))
        FileUtil.write_csv(df_macd, macd_file)
        FileUtil.write_csv(df_macd_data, macd_data_file, index=False)
        print('write_csv success')
    return df_macd, df_macd_data


def get_stock_n_month_macd(stock_id, month, read_csv=True, frequency='d', source='bao'):
    """
    获取macd
    :param stock_id:
    :param month:
    :param read_csv:
    :param frequency:
    :param source:
    :return:
    """
    macd_file = stock_month_file_macd.format(stock_id, frequency, month)
    macd_data_file = stock_month_file_macd_data.format(stock_id, frequency, month)
    if read_csv and FileUtil.exist_csv(macd_file) and FileUtil.exist_csv(macd_data_file):
        macd_result = FileUtil.read_csv(macd_file)
        macd_data_result = FileUtil.read_csv(macd_data_file)
        print('read_csv success')
        return macd_result, macd_data_result

    repository = stock_repository_factory.get(source)
    # k线数据
    result = repository.get_stock_data_n_month_age(stock_id, month, frequency)
    df_macd, df_macd_data = __get_data(result, frequency)

    # 写文件
    if read_csv:
        FileUtil.write_csv(result, stock_month_file_close.format(stock_id, frequency, month))
        FileUtil.write_csv(df_macd, macd_file)
        FileUtil.write_csv(df_macd_data, macd_data_file, index=False)
        print('write_csv success')
    return df_macd, df_macd_data


def get_bond_n_month_macd(stock_id, month, read_csv=True, frequency='d', source='ak'):
    """
    获取macd
    :param stock_id:
    :param month:
    :param read_csv:
    :param frequency:
    :param source:
    :return:
    """
    macd_file = bond_month_file_macd.format(stock_id, frequency, month)
    macd_data_file = bond_month_file_macd_data.format(stock_id, frequency, month)
    if read_csv and FileUtil.exist_csv(macd_file) and FileUtil.exist_csv(macd_data_file):
        macd_result = FileUtil.read_csv(macd_file)
        macd_data_result = FileUtil.read_csv(macd_data_file)
        print('read_csv success')
        return macd_result, macd_data_result

    repository = bond_repository_factory.get(source)
    # k线数据
    result = repository.get_bond_data_n_month_ago(stock_id, month, frequency)
    df_macd, df_macd_data = __get_data(result, frequency)

    # 写文件
    if read_csv:
        FileUtil.write_csv(result, bond_month_file_close.format(stock_id, frequency, month))
        FileUtil.write_csv(df_macd, macd_file)
        FileUtil.write_csv(df_macd_data, macd_data_file, index=False)
        print('write_csv success')
    return df_macd, df_macd_data
