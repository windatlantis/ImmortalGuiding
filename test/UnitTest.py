import math
import os
import unittest

import requests
import json
from numpy.random import randint
from pandas import Series, DataFrame
import baostock as bs
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import numpy as np
from main.utils.DateUtil import *
from main.repository import THSRepository

class MyTestCase(unittest.TestCase):

    def test_ths(self):
        stock_id = '123134.SZ'
        start_date = '2022-02-01'
        end_date = '2022-06-01'
        frequency = '5'
        request_url = 'https://quantapi.51ifind.com/api/v1/high_frequency'
        request_headers = {"Content-Type": "application/json", "access_token": THSRepository.get_access_token()}
        form_json = {"codes": stock_id, "indicators": "close", "starttime": start_date + " 09:15:00",
                     "endtime": end_date + " 15:15:00", "functionpara": {"Interval": frequency}}
        response = requests.post(url=request_url, json=form_json, headers=request_headers)
        content = json.loads(response.content)
        print(content)

    def test_arr(self):
        date_arr = ['date', 'aaa']
        columns = date_arr * 2 + ['zero_axis', 'cross_type', 'true_cross']
        column = ['code', 'buy_date', 'buy_time']
        part = ['sell_plan', 'sell_date']
        for i in range(2):
            column = column + [p + str(i) for p in part]
        print(column)
        # l = np.array(columns)
        # print(l[0])
        # for i in range(2 * 2 - 1, 0, -1):
        #     print(i)

    def test_date(self):
        day_str='2022-05-01'
        addition=-2
        days = []
        day = str2day(day_str)
        if addition > 0:
            for i in range(addition):
                days.append(day2str(day + dt.timedelta(days=i + 1)))
        else:
            for i in range(addition, 0):
                days.append(day2str(day + dt.timedelta(days=i)))
        print(days)
        time = calculate_time_float(20211129094500000, -15)
        print(time)

    def test_pandas(self):
        # data = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'])
        # data.insert(data.shape[1], 'd', 4)
        # data.insert(1, 'e', 5)
        # data['f'] = 0
        # data = pd.concat([data, pd.DataFrame(columns=['g'])], sort=False)
        # print(data)
        # print(data['a'][1:3].max())

        df = DataFrame(columns=('lib', 'qty1', 'qty2'))  # ????????????pandas???
        for i in range(6):  # ????????????
            df.loc[i] = [randint(-1, 1) for n in range(3)]
        df.loc[6] = [2, 1, 3]
        df.loc[df.shape[0]] = [3, 3, 3]
        print(df)

    def test_something(self):
        result = pd.read_csv("d:/20211001_20220125.csv")
        print(result)

    def test_series_getByName(self):
        stocks = {'????????????': '601318', '????????????': '000651', '????????????': '600036',
                  '????????????': '600030', '????????????': '600519'}
        Series_stocks = Series(stocks)
        print(Series_stocks)
        print("====")
        print(Series_stocks[['????????????']])
        s = pd.Series([1, 2, 3, 4, 5])
        # s = s.map(lambda x: x ** 2).apply(lambda x: x ** 2)
        # tmp = s.apply(lambda x: x ** 2)
        # for i in range(tmp.size):
        #     s[i] = tmp[i]
        custom_series_values(s, lambda x: x ** 2)
        print(s)

    def test_data_frame(self):
        # d = {'one': Series([1., 2., 3.], index=['a', 'b', 'c']),
        #      'two': Series([1., 2., 3., 4., ], index=['a', 'b', 'c', 'd']),
        #      'three': range(4),
        #      'four': 1.,
        #      'five': 'f'}
        # d = [1, 2, 3, 5, 6, 7, 9, 0]
        # df = DataFrame(d)
        # print(df)
        # print("DataFrame index:\n", df.index)
        # print("DataFrame columns:\n", df.columns)
        # print("DataFrame values:\n", df.values)
        classno = [1, 1, 1, 2, 2, 2]
        student = ['??????', '??????', '??????', '??????', '??????', '??????']
        chinese = [70, 80, 90, 20, 30, 40]
        english = [75, 85, 95, 35, 45, 55]
        math = [40, 50, 60, 70, 90, 80]
        physcis = [45, 55, 65, 65, 75, 85]
        dict = {'??????': classno, '??????': student, '??????': chinese, '??????': english, '??????': math, '??????': physcis}
        df = pd.DataFrame(dict)
        df = df.set_index(['??????', '??????'])
        df.columns = [['??????', '??????', '??????', '??????'], ['??????', '??????', '??????', '??????']]
        df.columns.names = ['??????', '??????']
        print(df)
        print(df.stack(-1))
        print(df.stack(0))
        print(df.stack(1))
        print(df.stack())


    def test_history_k(self):
        result = get_history_k()
        init_plt_style()

        result['close'].astype(float).plot(figsize=(12, 8))

        plt.title("??????????????????")
        plt.show()

    def test_ma(self):
        result = get_history_k()
        init_plt_style()

        # types = ['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA',
        #          'TRIMA', 'KAMA', 'MAMA', 'T3']
        # for i in range(len(types)):
        #     df_ma[types[i]] = ta.MA(close, timeperiod=5, matype=i)
        round2(result['close'])
        close = result['close']
        df_ma = pd.DataFrame(close)
        df_ma['MA20'] = ta.MA(close, timeperiod=20, matype=0)
        round2(df_ma['MA20'])
        plt.plot(df_ma)
        df_ma.to_csv(ma_file_path)

        # ??????
        plt.title('???????????????????????????????????????', fontsize=15)
        plt.xlabel('??????', fontsize=15)
        plt.show()


    def test_circle(self):
        # pivot???melt
        student = ['??????', '??????', '??????']
        chinese = [70, 80, 90]
        english = [75, 85, 95]
        math = [40, 50, 60]
        physcis = [45, 55, 65]
        dict = {'??????': student, '??????': chinese, '??????': english, '??????': math, '??????': physcis}
        df = pd.DataFrame(dict)
        # df = df.set_index(['??????'])
        # df.columns.names = ['??????']
        print(df)
        # df = df.stack()
        # print(df)
        print(df.melt(id_vars=['??????'], value_vars=['??????'], var_name='??????', value_name='??????'))
        # print(df.pivot(index=['??????', '??????', '??????', '??????'], columns='??????'))


    def test_macd(self):
        result = get_history_k(False)
        init_plt_style()

        round2(result['close'])
        close = result['close']
        # df_ma = pd.DataFrame(close)
        # df_ma['macd'] = ta.MACD(close)
        # round2(df_ma['macd'])a
        # plt.plot(df_ma)
        # df_ma.to_csv(macd_file_path)
        macdDIF, macdDEA, macd = ta.MACDEXT(close, fastperiod=12, fastmatype=1, slowperiod=26, slowmatype=1,
                                             signalperiod=9, signalmatype=1)
        macd = macd * 2
        df_macd = pd.DataFrame([macdDIF, macdDEA, macd], index=['dif', 'dea', 'macd'])
        # df_macd = pd.DataFrame(ta.MACD(close), index=['dif', 'dea', 'macd'])
        df_macd = df_macd.T
        df_macd.to_csv(macd_file_path)

        # ??????
        # plt.title('???????????????????????????????????????', fontsize=15)
        # plt.xlabel('??????', fontsize=15)
        # plt.show()


if __name__ == '__main__':
    unittest.main()

k_file_path = "d:/20210101_20220125.csv"
ma_file_path = "d:/ma_20210101_20220125.csv"
macd_file_path = "d:/macd_20210101_20220125.csv"


def get_history_k(read_csv=True):
    if read_csv and os.path.exists(k_file_path):
        result = pd.read_csv(k_file_path)
        # ????????????
        result.index = pd.to_datetime(result['date'])
        return result

    #### ???????????? ####
    lg = bs.login()
    # ????????????????????????
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    #### ????????????A?????????K????????? ####
    # ??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
    # ??????????????????date,time,code,open,high,low,close,volume,amount,adjustflag
    # ??????????????????date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    rs = bs.query_history_k_data_plus("sh.000001",
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                      start_date='2021-01-01', end_date='2022-01-25',
                                      frequency="d", adjustflag="3")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### ???????????? ####
    bs.logout()

    #### ????????? ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # ?????????????????????????????????????????????
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    # ?????????
    result.to_csv(k_file_path)
    # ????????????
    result.index = pd.to_datetime(result['date'])

    return result


def init_plt_style():
    large = 22
    med = 16
    small = 12
    params = {
        'legend.fontsize': med,
        'figure.figsize': (16, 10),
        'axes.labelsize': med,
        'axes.titlesize': med,
        'xtick.labelsize': med,
        'ytick.labelsize': med,
        'figure.titlesize': large}
    plt.rcParams.update(params)
    plt.style.use('seaborn-whitegrid')
    # ??????matplotlib??????????????????
    plt.rcParams['font.sans-serif'] = ['SimHei']  # ?????????????????????
    plt.rcParams['axes.unicode_minus'] = False
    # ??????
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')


def round2(series: Series):
    custom_series_values(series, lambda x: round(float(x), 2))

    return


def custom_series_values(series: Series, func):
    for i in range(series.size):
        series.values[i] = func(series.values[i])

    return

