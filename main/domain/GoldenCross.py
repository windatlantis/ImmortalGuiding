# -*- coding:utf-8 -*-
"""
@Time : 2022/3/5 10:43
@Author: windatlantis
@File : GoldenCross.py
"""
from main.repository.BaoStockRepository import BaoStockRepository
from main.service import TaLibService, MatplotService
from main.utils import SeriesUtil
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta

def get_macd():
    bao = BaoStockRepository()
    result = bao.get_stock_data_pass_year('sh.601398')
    result.to_csv('d:/600036.csv')
    MatplotService.init_plt_style()

    # 小数点后两位
    SeriesUtil.round2(result['close'])
    close = result['close']

    # 获取3条线的数据
    macdDIF, macdDEA, macd = TaLibService.get_macd(close)
    # 前33个为Nan，所以推荐用于计算的数据量一般为你所求日期之间数据量的3倍
    df_macd = pd.DataFrame([macdDIF[33:], macdDEA[33:], macd[33:]], index=['dif', 'dea', 'macd'])
    # 转置
    df_macd = df_macd.T
    df_macd.to_csv('d:/600036_macd.csv')
    return df_macd


def draw_macd_pic(df_macd):
    # 绘制图片
    MatplotService.show(df_macd, title='招商银行近一年macd', xlabel='时间', legends=['dif', 'dea', 'macd'])

def print_gloden_cross():
    df_macd = get_macd()
    draw_macd_pic(df_macd)


def greaterThan(a, b):
    if (not a) | (not b):
        return True
    elif (a > b):
        return True
    else:
        return False

def computeMACD():
    bao = BaoStockRepository()
    code = 'sh.600036'
    df = bao.get_stock_data_n_year_ago(code, 5)
    #剔除停盘数据
    #print(df)
    df2 = df[df['tradestatus']=='1']#交易日
    #获取dif,dea,hist，它们的数据类似是tuple，且跟df2的date日期一一对应
    #记住了dif,dea,hist前33个为Nan，所以推荐用于计算的数据量一般为你所求日期之间数据量的3倍
    #这里计算的hist就是dif-dea,而很多证券商计算的MACD=hist*2=(dif-dea)*2
    dif, dea, hist= ta.MACD(df2['close'].astype(float).values, fastperiod=12, slowperiod=26, signalperiod=9)
    df3 = pd.DataFrame({'dif':dif[33:],'dea':dea[33:],'hist':hist[33:]},
                       index=df2['date'][33:],columns=['dif','dea','hist'])
    df4 = pd.merge(df3, df2, on='date', how='left')
    #print(df)
    print(df2)
    print(df3)
    print(df4)
    df4.to_csv("D:/out_df4.csv", index=False)
    df2.to_csv("D:/out_df2.csv", index=False)
    hist=2*(df4['dif']-df4['dea'])
    df3.plot(title='MACD')
    plt.show()
    #寻找MACD金叉和死叉
    datenumber = int(df3.shape[0])
    lastdif=None
    lastclose = None
    #tlist = []
    print(df3.iloc[0,0])
    for i in range(datenumber-1):
        if (df4.iloc[i, 1]<=df4.iloc[i, 2])&\
                (df4.iloc[i+1, 1]>=df4.iloc[i+1, 2])&\
                    greaterThan(lastdif, df4.iloc[i+1,1]) &\
                        greaterThan(df4['close'][i+1],lastclose):#上一次下穿时间的收盘价小于当日收盘价
                lastdif = df4.iloc[i , 1]
                lastclose = df4['close'][i]
                #tlist.append(df3.index[i+1])
                print("期货代码:{},顶背离时间：{}, 价格：{}".format(code,df4['date'][i + 1], df4['close'][i+1]))
        if ((df4.iloc[i,1]>=df4.iloc[i,2])&(df4.iloc[i+1,1]<=df4.iloc[i+1,2])&greaterThan(df4.iloc[i+1,1],lastdif) &greaterThan(lastclose,df4['close'][i+1])):
            lastdif = df4['dif'][i]
            lastclose = df4['close'][i]
            #tlist.append(df4['date'][i+1])
            print("期货代码:{},底背离时间：{}, 价格：{}".format(code, df4['date'][i + 1], df4['close'][i+1]))

