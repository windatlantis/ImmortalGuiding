import math
import os
import unittest

from pandas import Series, DataFrame
import baostock as bs
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import numpy as np


class MyTestCase(unittest.TestCase):

    def test_something(self):
        result = pd.read_csv("d:/20211001_20220125.csv")
        print(result)

    def test_series_getByName(self):
        stocks = {'中国平安': '601318', '格力电器': '000651', '招商银行': '600036',
                  '中信证券': '600030', '贵州茅台': '600519'}
        Series_stocks = Series(stocks)
        print(Series_stocks)
        print("====")
        print(Series_stocks[['中国平安']])
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
        student = ['张三', '李四', '王五', '刘六', '唐七', '赵八']
        chinese = [70, 80, 90, 20, 30, 40]
        english = [75, 85, 95, 35, 45, 55]
        math = [40, 50, 60, 70, 90, 80]
        physcis = [45, 55, 65, 65, 75, 85]
        dict = {'班级': classno, '学生': student, '语文': chinese, '英语': english, '数学': math, '物理': physcis}
        df = pd.DataFrame(dict)
        df = df.set_index(['班级', '学生'])
        df.columns = [['文科', '文科', '理科', '理科'], ['语文', '英语', '数学', '物理']]
        df.columns.names = ['文理', '科目']
        print(df)
        print(df.stack(-1))
        print(df.stack(0))
        print(df.stack(1))
        print(df.stack())


    def test_history_k(self):
        result = get_history_k()
        init_plt_style()

        result['close'].astype(float).plot(figsize=(12, 8))

        plt.title("上证指数走势")
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

        # 标题
        plt.title('上证指数各种类型移动平均线', fontsize=15)
        plt.xlabel('时间', fontsize=15)
        plt.show()


    def test_circle(self):
        # pivot和melt
        student = ['张三', '李四', '王五']
        chinese = [70, 80, 90]
        english = [75, 85, 95]
        math = [40, 50, 60]
        physcis = [45, 55, 65]
        dict = {'学生': student, '语文': chinese, '英语': english, '数学': math, '物理': physcis}
        df = pd.DataFrame(dict)
        # df = df.set_index(['学生'])
        # df.columns.names = ['学科']
        print(df)
        # df = df.stack()
        # print(df)
        print(df.melt(id_vars=['学生'], value_vars=['语文'], var_name='学科', value_name='成绩'))
        # print(df.pivot(index=['语文', '英语', '数学', '物理'], columns='学生'))


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

        # 标题
        # plt.title('上证指数各种类型移动平均线', fontsize=15)
        # plt.xlabel('时间', fontsize=15)
        # plt.show()


if __name__ == '__main__':
    unittest.main()

k_file_path = "d:/20210101_20220125.csv"
ma_file_path = "d:/ma_20210101_20220125.csv"
macd_file_path = "d:/macd_20210101_20220125.csv"


def get_history_k(read_csv=True):
    if read_csv and os.path.exists(k_file_path):
        result = pd.read_csv(k_file_path)
        # 日期排序
        result.index = pd.to_datetime(result['date'])
        return result

    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    rs = bs.query_history_k_data_plus("sh.000001",
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                      start_date='2021-01-01', end_date='2022-01-25',
                                      frequency="d", adjustflag="3")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### 登出系统 ####
    bs.logout()

    #### 结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    # 写文件
    result.to_csv(k_file_path)
    # 日期排序
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
    # 设置matplotlib正常显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False
    # 边框
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

