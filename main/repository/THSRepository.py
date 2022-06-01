# -*- coding:utf-8 -*-
"""
@Time : 2022/6/1 22:39
@Author: windatlantis
@File : THSRepository.py
"""

import requests
import json
import pandas as pd
from pandas import DataFrame
from main.repository import RepoConstants

from main.repository.IRepository import IStockRepository, IBondRepository
from main.utils import DateUtil

bond_day_fields = ['date', 'code', 'close']
bond_min_fields = ['date', 'time', 'code', 'close']


def get_access_token():
    getAccessTokenUrl = 'https://ft.10jqka.com.cn/api/v1/get_access_token'
    refreshToken = 'eyJzaWduX3RpbWUiOiIyMDIyLTA2LTAxIDIyOjM2OjQ3In0=.eyJ1aWQiOiI2MzU4MDMzNTYifQ==.41523B88022C391A4CC3ED305D0F720E0E74A048A6F75F7B68272BFF365FAB07'
    getAccessTokenHeader = {"ContentType": "application/json", "refresh_token": refreshToken}
    getAccessTokenResponse = requests.post(url=getAccessTokenUrl, headers=getAccessTokenHeader)
    accessToken = json.loads(getAccessTokenResponse.content)['data']['access_token']
    print(accessToken)
    return accessToken


def data_convert(rs: DataFrame, stock_id, time='daily'):
    if time in RepoConstants.ak_frequency or time in RepoConstants.bao_frequency:
        code_arr = [stock_id for i in range(rs.shape[0])]
        rs.insert(1, 'code', code_arr)
    else:
        rs['date'] = rs['date'] + ':00'
        copy = rs.copy()
        copy['time'] = copy['date'].apply(lambda x: DateUtil.date2time(DateUtil.str2day(x, DateUtil.yymmdd_hhmmss)))
        copy['date'] = copy['date'].apply(lambda x: DateUtil.str2day(x, DateUtil.yymmdd_hhmmss).date())
        code_arr = [stock_id for i in range(rs.shape[0])]
        copy.insert(1, 'code', code_arr)
        copy = copy[bond_min_fields]
        rs = copy.copy()
    return rs


class THSStockRepository(IStockRepository):

    def get_stock_data_by_date(self, stock_id, start_date, end_date, frequency='d'):
        pass


class THSBondRepository(IBondRepository):

    def __init__(self):
        self.__refresh_token()

    def __refresh_token(self):
        self.access_token = get_access_token()

    def get_bond_data_daily(self, stock_id, start_date, end_date, frequency='d'):
        request_url = 'https://quantapi.51ifind.com/api/v1/cmd_history_quotation'
        request_headers = {"Content-Type": "application/json", "access_token": self.access_token}
        form_json = {"codes": stock_id, "indicators": "close", "startdate": start_date,
                     "enddate": end_date, "functionpara": {"PriceType": "1"}}
        response = requests.post(url=request_url, json=form_json, headers=request_headers)
        content = json.loads(response.content)
        print(content)
        code = content['errorcode']
        if code == 0:
            bond_table = pd.DataFrame(columns=['date', 'close'])
            table = content['tables'][0]
            bond_table['date'] = table['time']
            bond_table['close'] = table['table']['close']
            return data_convert(bond_table, stock_id, frequency)
        elif code == -1010:
            self.__refresh_token()
            return self.get_bond_data_daily(stock_id, start_date, end_date, frequency)
        else:
            print('error:' + code + ', msg:' + content['errmsg'])
            return None

    def get_bond_data_min(self, stock_id, start_date, end_date, frequency='5'):
        request_url = 'https://quantapi.51ifind.com/api/v1/high_frequency'
        request_headers = {"Content-Type": "application/json", "access_token": self.access_token}
        form_json = {"codes": stock_id, "indicators": "close", "starttime": start_date + " 09:15:00",
                     "endtime": end_date + " 15:15:00", "functionpara": {"Interval": frequency}}
        response = requests.post(url=request_url, json=form_json, headers=request_headers)
        content = json.loads(response.content)
        print(content)
        code = content['errorcode']
        if code == 0:
            bond_table = pd.DataFrame(columns=['date', 'close'])
            table = content['tables'][0]
            bond_table['date'] = table['time']
            bond_table['close'] = table['table']['close']
            return data_convert(bond_table, stock_id, frequency)
        elif code == -1010:
            self.__refresh_token()
            return self.get_bond_data_min(stock_id, start_date, end_date, frequency)
        else:
            print('error:' + code + ', msg:' + content['errmsg'])
            return None
