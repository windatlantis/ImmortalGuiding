# -*- coding:utf-8 -*-
"""
@Time : 2022/5/14 15:54
@Author: windatlantis
@File : Day15mStrategy.py
"""

from main.domain import Analysiser, DataMemHolder
from main.strategy.Day15TradeStrategy import Day15TradeStrategy
from main.trader.Trader import Trader

k_type_date_list = ['m', 'w', 'd']
k_type_time_list = ['60m', '15m', '5m']
k_type_time_map = {
    'm': 'date',
    'w': 'date',
    'd': 'date',
    '60m': 'time',
    '15m': 'time',
    '5m': 'time',
}


def day_15min(stock_id, is_stock=True):
    """
    日-15金叉套
    :param stock_id:
    :param is_stock:
    :return:
    """
    trader = Trader()
    strategy = Day15TradeStrategy()
    strategy.load_trader(trader)
    if is_stock:
        holder = DataMemHolder.get_stock_from_mem(stock_id)
    else:
        holder = DataMemHolder.get_bond_from_mem(stock_id)
    print('ready to action ' + stock_id)
    for i in range(1, holder.day_macd_data.shape[0]):
        cur = holder.day_macd_data.iloc[i]
        day = cur['date']
        strategy.load_data(stock_id, day, is_stock)
        day_5min = holder.min5_macd_data[holder.min5_macd_data['date'] == day]
        for j in range(day_5min.shape[0]):
            cur_ = day_5min.iloc[j]
            min5 = cur_['time']
            strategy.match(day, min5, cur_['close'])
    print('start handle record ' + stock_id)
    record_list = trader.record_map.get(stock_id)
    record_list = handle_record(record_list)
    print(record_list)
    Analysiser.save_record(record_list, stock_id)


def handle_record(record_list):
    """
    处理买卖记录
    :param record_list:
    :return:
    """
    if record_list is None:
        print('record_list is None')
        return None
    record_list = record_list.sort_values('time')
    tips = []
    stocks = []
    stock = 0
    for j in range(record_list.shape[0]):
        cur = record_list.iloc[j]
        last = record_list.iloc[j - 1]
        tip = ''
        if 'sell' in cur['operation']:
            if stock == 0:
                tip = 'buy first'
            else:
                stock = 0
        elif 'buy' in cur['operation']:
            stock += 1
        if j > 1 and len(tip) == 0 and len(cur['operation']) == len(last['operation']):
            tip = 'repeat'
        tips.append(tip)
        stocks.append(stock)
    record_list.insert(record_list.shape[1], 'tips', tips)
    record_list.insert(record_list.shape[1], 'stocks', stocks)
    return record_list
