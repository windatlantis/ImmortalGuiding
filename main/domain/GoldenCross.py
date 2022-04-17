# -*- coding:utf-8 -*-
"""
@Time : 2022/3/5 10:43
@Author: windatlantis
@File : GoldenCross.py
"""
import os

from pandas import DataFrame
from main.repository.BaoStockRepository import BaoStockRepository
from main.service import TaLibService, MatplotService
from main.utils import CollectionUtil
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta


def print_cross_useful(stock_id, read_csv=True):
    """
    打印金叉、死叉
    :param stock_id:
    :param read_csv:
    :return:
    """
    df_macd, df_macd_data = get_macd(stock_id, read_csv)
    # draw_macd_pic(df_macd, stock_id)
    print_cross(df_macd_data)


def get_macd(stock_id, read_csv=True):
    """
    获取macd
    :param stock_id:
    :param read_csv:
    :return:
    """
    macd_file_path = 'd:/' + stock_id + '_macd.csv'
    macd_data_file_path = 'd:/' + stock_id + '_macd_data.csv'
    if read_csv:
        macd_result = None
        macd_data_result = None
        if os.path.exists(macd_file_path):
            macd_result = pd.read_csv(macd_file_path)

        if os.path.exists(macd_data_file_path):
            macd_data_result = pd.read_csv(macd_data_file_path)

        return macd_result, macd_data_result

    bao = BaoStockRepository()
    # k线数据
    result = bao.get_stock_data_n_year_ago(stock_id, 5)
    result.to_csv('d:/' + stock_id + '.csv')

    # 获取3条线的数据
    macdDIF, macdDEA, macd = TaLibService.get_macd(result['close'].astype(float).values)
    # 小数点后两位
    CollectionUtil.round2(macdDIF)
    CollectionUtil.round2(macdDEA)
    CollectionUtil.round2(macd)
    # 前33个为Nan，所以推荐用于计算的数据量一般为你所求日期之间数据量的3倍
    df_macd = pd.DataFrame({"dif": macdDIF[33:], "dea": macdDEA[33:], "macd": macd[33:]}, index=result['date'][33:],
                           columns=['dif', 'dea', 'macd'])
    df_macd.to_csv(macd_file_path)
    # 与原数据合并
    df_macd_data = pd.merge(df_macd, result, on='date', how='left')
    df_macd_data.to_csv(macd_data_file_path, index=False)
    return df_macd, df_macd_data


def draw_macd_pic(df_macd, stock_id):
    """
    绘制macd图
    :param df_macd:
    :param stock_id:
    :return:
    """
    MatplotService.init_plt_style()
    # 绘制图片
    MatplotService.show(df_macd, title=stock_id + '近一年macd', xlabel='时间', legends=['dif', 'dea', 'macd'])


def print_cross(df_macd_data):
    """
    打印交叉数据及背离数据
    :param df_macd_data:
    :return:
    """
    line_number = int(df_macd_data.shape[0])
    df_macd_data_extend = pd.DataFrame(columns=['date', '30day_min_close', '30day_max_close',
                                                '30day_new_low', '30day_new_high',
                                                'price_last_low', 'price_last_high',
                                                'dif_last_low', 'dif_last_high'])
    price_last_low = None
    price_last_high = None
    dif_last_low = None
    dif_last_high = None
    for i in range(line_number):
        # 当前
        cur = df_macd_data.iloc[i]
        cur_close = cur['close']
        cur_dif = cur['dif']
        # 前高、前低
        if i > 2:
            if cur_close < df_macd_data['close'][i - 1] and df_macd_data['close'][i - 1] > df_macd_data['close'][i - 2]:
                price_last_high = df_macd_data['close'][i - 1]
            elif cur_close > df_macd_data['close'][i - 1] and df_macd_data['close'][i - 1] < df_macd_data['close'][i - 2]:
                price_last_low = df_macd_data['close'][i - 1]
            if cur_dif < df_macd_data['dif'][i - 1] and df_macd_data['dif'][i - 1] > df_macd_data['dif'][i - 2]:
                dif_last_high = df_macd_data['dif'][i - 1]
            elif cur_dif > df_macd_data['dif'][i - 1] and df_macd_data['dif'][i - 1] < df_macd_data['dif'][i - 2]:
                dif_last_low = df_macd_data['dif'][i - 1]
        # 30天内
        thirty_day_ago_idx = 0 if i <= 29 else i - 29
        thirty_day_min_close = df_macd_data['close'][thirty_day_ago_idx:i + 1].min()
        thirty_day_max_close = df_macd_data['close'][thirty_day_ago_idx:i + 1].max()
        # add
        df_macd_data_extend.loc[i] = {'date': cur['date'],
                                      '30day_min_close': thirty_day_min_close, '30day_max_close': thirty_day_max_close,
                                      '30day_new_low': 1 if cur_close == thirty_day_min_close else 0,
                                      '30day_new_high': 1 if cur_close == thirty_day_max_close else 0,
                                      'price_last_low': price_last_low, 'price_last_high': price_last_high,
                                      'dif_last_low': dif_last_low, 'dif_last_high': dif_last_high}

    # merge
    merge_result = pd.merge(df_macd_data, df_macd_data_extend, on='date', how='left')
    print(merge_result)
    print(get_beili(merge_result))


def get_beili(data: DataFrame):
    """
    获取背离
    :param data:
    :return:
    """
    line = int(data.shape[0])
    beili_collector = pd.DataFrame(columns=['date', 'close', 'macd_type'])
    for i in range(line):
        cur = data.iloc[i]
        cur_close = cur['close']
        macd_type = None

        if cur['price_last_high'] is not None and cur['price_last_low'] is not None and cur['dif_last_high'] is not None and cur['dif_last_low'] is not None:
            if cur['30day_new_high'] == 1 and cur_close > cur['price_last_high'] and cur['dif'] < cur['dif_last_high']:
                macd_type = '顶背离'
            elif cur['30day_new_low'] == 1 and cur_close < cur['price_last_low'] and cur['dif'] > cur['dif_last_low']:
                macd_type = '底背离'

        if macd_type is not None:
            beili_collector.loc[i] = {'date': cur['date'], 'close': cur_close, 'macd_type': macd_type}

    return beili_collector


def greaterThan(a, b):
    if (not a) | (not b):
        return True
    elif (a > b):
        return True
    else:
        return False


def computeMACD(stock_id):
    bao = BaoStockRepository()
    df = bao.get_stock_data_n_year_ago(stock_id, 5)
    # 剔除停盘数据
    # print(df)
    df2 = df[df['tradestatus'] == '1']  # 交易日
    # 获取dif,dea,hist，它们的数据类似是tuple，且跟df2的date日期一一对应
    # 记住了dif,dea,hist前33个为Nan，所以推荐用于计算的数据量一般为你所求日期之间数据量的3倍
    # 这里计算的hist就是dif-dea,而很多证券商计算的MACD=hist*2=(dif-dea)*2
    dif, dea, hist = ta.MACD(df2['close'].astype(float).values, fastperiod=12, slowperiod=26, signalperiod=9)
    hist *= 2
    df3 = pd.DataFrame({'dif': dif[33:], 'dea': dea[33:], 'hist': hist[33:]},
                       index=df2['date'][33:], columns=['dif', 'dea', 'hist'])
    df4 = pd.merge(df3, df2, on='date', how='left')
    # print(df)
    # print(df2)
    # print(df3)
    print(df4)
    df3 = df3[900:]
    df2.to_csv("D:/out_df2.csv")
    df3.to_csv("D:/out_df3.csv")
    df4.to_csv("D:/out_df4.csv", index=False)
    # hist=2*(df4['dif']-df4['dea'])
    df3.plot(title='MACD')
    plt.show()
    # 寻找MACD金叉和死叉
    datenumber = int(df3.shape[0])
    lastdif = None
    lastclose = None
    # tlist = []
    print(df3.iloc[0, 0])
    for i in range(datenumber - 1):
        if (df4.iloc[i, 1] <= df4.iloc[i, 2]) & \
                (df4.iloc[i + 1, 1] >= df4.iloc[i + 1, 2]) & \
                greaterThan(lastdif, df4.iloc[i + 1, 1]) & \
                greaterThan(df4['close'][i + 1], lastclose):  # 上一次下穿时间的收盘价小于当日收盘价
            lastdif = df4.iloc[i, 1]
            lastclose = df4['close'][i]
            # tlist.append(df3.index[i+1])
            print("期货代码:{},顶背离时间：{}, 价格：{}".format(stock_id, df4['date'][i + 1], df4['close'][i + 1]))
        if ((df4.iloc[i, 1] >= df4.iloc[i, 2]) & (df4.iloc[i + 1, 1] <= df4.iloc[i + 1, 2]) & greaterThan(
                df4.iloc[i + 1, 1], lastdif) & greaterThan(lastclose, df4['close'][i + 1])):
            lastdif = df4['dif'][i]
            lastclose = df4['close'][i]
            # tlist.append(df4['date'][i+1])
            print("期货代码:{},底背离时间：{}, 价格：{}".format(stock_id, df4['date'][i + 1], df4['close'][i + 1]))
