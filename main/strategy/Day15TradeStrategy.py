# -*- coding:utf-8 -*-
"""
@Time : 2022/5/28 14:14
@Author: windatlantis
@File : Day15TradeStrategy.py
"""

import pandas as pd
import numpy as np

from main.strategy.IStrategy import ITradeStrategy
from main.domain import DataMemHolder
from main.service import LineCrossService, DeviationService
from main.trader.ITrader import ITrader
from main.utils import CollectionUtil, DateUtil

mode_day_15min_sell = 1
mode_day_60min_sell = 2
occurrence_time_60_dead_soon = 'et60ds'
occurrence_time_15_top_deviation = 'et15td'
occurrence_time_15_dead_soon = 'et15ds'
occurrence_time_5_top_deviation = 'et5td'
occurrence_time_15_golden_soon = 'et15gs'
occurrence_time_5_bottom_deviation = 'et5bd'


class Day15TradeStrategy(ITradeStrategy):

    def __init__(self):
        self.__stock_id = ''
        self.__mode = mode_day_15min_sell
        self.__mem_holder = None
        self.__trader: ITrader = None
        self.__trade_days = None
        self.__golden_cross_days = []
        self.__day_macd_data = None

        # -- 模式1
        # 5分钟级别macd
        self.__macd_5 = None
        # 15分钟级别macd
        self.__macd_15 = None
        # 当天15分钟级别macd
        self.__macd_15_day = None
        # 15分钟级别金叉死叉
        self.__line_cross_15 = None
        self.__line_cross_soon_15 = None
        # 5分钟级别金叉死叉
        self.__line_cross_5 = None
        # 5分钟级别背离
        self.__macd_deviation_5 = None

        # -- 模式2
        # 60分钟级别macd
        self.__macd_60 = None
        # 当天60分钟级别macd
        self.__macd_60_day = None
        # 60分钟级别金叉死叉
        self.__line_cross_60 = None
        self.__line_cross_soon_60 = None
        # 15分钟级别背离
        self.__macd_deviation_15 = None
        # 有效时间
        self.__effective_time = {}

    def load_data(self, stock_id, day, is_stock):
        self.__stock_id = stock_id
        if is_stock:
            self.__mem_holder = DataMemHolder.get_stock_from_mem(stock_id)
        else:
            self.__mem_holder = DataMemHolder.get_bond_from_mem(stock_id)
        day_macd_data = self.__mem_holder.day_macd_data
        min5_macd_data = self.__mem_holder.min5_macd_data
        min15_macd_data = self.__mem_holder.min15_macd_data
        min60_macd_data = self.__mem_holder.min60_macd_data
        self.__trade_days = day_macd_data['date'].unique()

        for i in range(1, day_macd_data.shape[0]):
            cur = day_macd_data.iloc[i]
            last = day_macd_data.iloc[i - 1]
            # 日线macd金叉及其延申
            if cur['macd'] > 0 and cur['macd'] >= last['macd']:
                self.__golden_cross_days.append(cur['date'])

        # 今天及前3天，共四天
        idx_tuple = np.where(self.__trade_days == day)
        if len(idx_tuple) == 0:
            date_range = self.__trade_days[-4:]
        else:
            idx = idx_tuple[0][0]
            date_range = self.__trade_days[idx - 3: idx + 1]

        # 5分钟级别macd
        self.__macd_5 = pd.DataFrame(columns=min5_macd_data.columns)
        # 15分钟级别macd
        self.__macd_15 = pd.DataFrame(columns=min15_macd_data.columns)
        # 60分钟级别macd
        self.__macd_60 = pd.DataFrame(columns=min60_macd_data.columns)
        for j in range(len(date_range)):
            CollectionUtil.df_add(self.__macd_5, min5_macd_data[min5_macd_data['date'] == date_range[j]])
            CollectionUtil.df_add(self.__macd_15, min15_macd_data[min15_macd_data['date'] == date_range[j]])
            CollectionUtil.df_add(self.__macd_60, min60_macd_data[min60_macd_data['date'] == date_range[j]])

        # 当天15分钟级别macd
        self.__macd_15_day = min15_macd_data[min15_macd_data['date'] == day]
        # 当天60分钟级别macd
        self.__macd_60_day = min60_macd_data[min60_macd_data['date'] == day]
        # 15分钟级别金叉死叉
        self.__line_cross_15 = LineCrossService.line_cross(self.__macd_15, date_name='time')
        self.__line_cross_soon_15 = LineCrossService.line_cross_soon(self.__macd_15, date_name='time')
        # 5分钟级别金叉死叉
        self.__line_cross_5 = LineCrossService.line_cross(self.__macd_5, date_name='time')
        # 5分钟级别背离
        self.__macd_deviation_5 = DeviationService.collect_macd_deviation(self.__line_cross_5, date_name='time')

        # 60分钟级别金叉死叉
        self.__line_cross_60 = LineCrossService.line_cross(self.__macd_60, date_name='time')
        self.__line_cross_soon_60 = LineCrossService.line_cross_soon(self.__macd_60, date_name='time')
        # 15分钟级别背离
        self.__macd_deviation_15 = DeviationService.collect_macd_deviation(self.__line_cross_15, date_name='time')

    def load_trader(self, trader: ITrader):
        self.__trader = trader

    def match(self, day, time, price):
        """
        匹配买卖点
        :param day:
        :param time:
        :param price:
        :return:
        """
        golden_cross_day = day in self.__golden_cross_days
        if golden_cross_day:
            self.__day_15min_buy2(day, time, price)
            self.__day_15min_buy1(day, time, price)
        if self.__mode == mode_day_15min_sell:
            self.__day_15min_sell(day, time, price)
        elif self.__mode == mode_day_60min_sell:
            self.__day_60min_sell(day, time, price)

    def __change_mode(self, mode):
        """
        切换卖出模式
        :param mode:
        :return:
        """
        self.__mode = mode

    def __zero_axis_60(self, cur_time):
        """
        60分钟macd的dif
        :param cur_time:
        :return:
        """
        return self.__macd_60_day[
            (DateUtil.calculate_time_float(cur_time, 60) > self.__macd_60_day['time']) & (
                    cur_time <= self.__macd_60_day['time'])]['dif'].iloc[0]

    def __delay_judge_point(self, self_symbol, other_symbol, cur_time, between_time, success_action):
        """
        延迟判断是否买卖点
        :param self_symbol: 自己的缓存key
        :param other_symbol: 另一个条件的缓存key
        :param cur_time:
        :param between_time: 延迟时间
        :param success_action:
        :return:
        """
        if other_symbol in self.__effective_time:
            if DateUtil.between_minutes(self.__effective_time.get(other_symbol), cur_time,
                                        self.__mem_holder.trade_date) <= between_time:
                success_action()
            self.__effective_time.pop(other_symbol)
        else:
            self.__effective_time[self_symbol] = cur_time

    def __delay_judge_point2(self, self_symbol, other_symbol, cur_time, between_time, need_check_mode_2,
                             success_action):
        """
        延迟判断是否买卖点
        :param self_symbol: 自己的缓存key
        :param other_symbol: 另一个条件的缓存key
        :param cur_time:
        :param between_time: 延迟时间
        :param need_check_mode_2:
        :param success_action:
        :return:
        """
        if other_symbol in self.__effective_time:
            if DateUtil.between_minutes(self.__effective_time.get(other_symbol), cur_time,
                                        self.__mem_holder.trade_date) <= between_time:
                if need_check_mode_2 and self.__macd_60_day[
                    (DateUtil.calculate_time_float(cur_time, 60) > self.__macd_60_day['time']) & (
                            cur_time <= self.__macd_60_day['time'])]['dif'].iloc[0] > 0:
                    print(f'{cur_time} should sell4, but macd_60_day')
                    self.__change_mode(mode_day_60min_sell)
                else:
                    success_action()
            self.__effective_time.pop(other_symbol)
        else:
            self.__effective_time[self_symbol] = cur_time

    def __day_15min_buy1(self, day, time, price):
        """
        买入信号1：【日线macd金叉，且开口向上】【15分钟金叉，在0轴或0轴以下】。
        :param day:
        :param time:
        :return:
        """
        # 15分钟线金叉
        golden_cross = LineCrossService.filter_golden_cross(self.__line_cross_15)
        if golden_cross.empty:
            return
        # 【15分钟金叉，在0轴或0轴以下】
        if time in golden_cross['time'].unique() and golden_cross[golden_cross['time'] == time].iloc[0][
            'zero_axis'] <= 0:
            self.__trader.buy(self.__stock_id, day, time, price, 'buy1', zero_axis_60=self.__zero_axis_60(time))

    def __day_15min_buy2(self, day, time, price):
        """
        买入信号2：【日线macd金叉，且开口向上】【15分钟即将金叉，在0轴或0轴以下】，【5分钟级别底背离】。
        :param day:
        :param time:
        :return:
        """
        # 15分钟即将金叉
        golden_cross_15 = LineCrossService.filter_golden_cross_soon(self.__line_cross_soon_15)
        # 5分钟级别底背离
        bottom_deviation_5 = DeviationService.filter_macd_bottom_deviation(self.__macd_deviation_5)
        if golden_cross_15.empty or bottom_deviation_5.empty:
            return
        # 【15分钟即将金叉，在0轴或0轴以下】
        if time in golden_cross_15['time'].unique() and golden_cross_15[golden_cross_15['time'] == time].iloc[0][
            'zero_axis'] < 0:
            func = lambda: self.__trader.buy(self.__stock_id, day, time, price, 'buy2',
                                             zero_axis_60=self.__zero_axis_60(time))
            self.__delay_judge_point(occurrence_time_15_golden_soon, occurrence_time_5_bottom_deviation, time, 15, func)
        # 【5分钟级别底背离】
        if time in bottom_deviation_5['time'].unique():
            func = lambda: self.__trader.buy(self.__stock_id, day, time, price, 'buy2',
                                             zero_axis_60=self.__zero_axis_60(time))
            self.__delay_judge_point(occurrence_time_5_bottom_deviation, occurrence_time_15_golden_soon, time, 15, func)

    def __day_15min_sell(self, day, time, price):
        """
        信号一：【15分钟级别，在0轴以下】，【5分钟死叉】。——每5min判断一次
        信号二：【15分钟级别，在0轴以上】，【5分钟顶背离 且 15分钟即将死叉】（只要30分钟内两个条件都出现即可），最后，【15分钟出现死叉】一定卖出。
        :param day:
        :param time:
        :return:
        """
        # 先买入才能卖出
        last_record = self.__trader.last_record(self.__stock_id)
        if last_record is None or 'sell' in last_record['operation']:
            return True
        # 加载条件*所需数据
        need_check_mode_2 = last_record['zero_axis_60'] < 0
        # 正常卖出条件
        dead_cross_5 = LineCrossService.filter_dead_cross(self.__line_cross_5)['time'].unique()
        dead_cross_soon_15 = LineCrossService.filter_dead_cross_soon(self.__line_cross_soon_15)['time'].unique()
        top_deviation_5 = DeviationService.filter_macd_top_deviation(self.__macd_deviation_5)['time'].unique()
        dead_cross_15 = LineCrossService.filter_dead_cross(self.__line_cross_15)['time'].unique()

        last_15_minutes = DateUtil.last_15_minutes_time_float(time)
        temp = self.__macd_15_day
        if self.__macd_15_day[self.__macd_15_day['time'] == last_15_minutes].iloc[0]['dif'] <= 0:
            # 【15分钟级别，在0轴以下】，【5分钟死叉】
            if time in dead_cross_5:
                self.__trader.sell(self.__stock_id, day, time, price, 'sell3')
        else:
            origin_mode = self.__mode
            # 【15分钟级别，在0轴以上】
            # 【15分钟即将死叉】
            if time in dead_cross_soon_15:
                func = lambda: self.__trader.sell(self.__stock_id, day, time, price, 'sell4')
                self.__delay_judge_point2(occurrence_time_15_dead_soon, occurrence_time_5_top_deviation, time, 30,
                                          need_check_mode_2, func)
                if not origin_mode == self.__mode:
                    return
            # 【5分钟顶背离】
            if time in top_deviation_5:
                func = lambda: self.__trader.sell(self.__stock_id, day, time, price, 'sell4')
                self.__delay_judge_point2(occurrence_time_5_top_deviation, occurrence_time_15_dead_soon, time, 30,
                                          need_check_mode_2, func)
                if not origin_mode == self.__mode:
                    return
            # 【15分钟出现死叉】一定卖出
            if time in dead_cross_15:
                if need_check_mode_2 and self.__macd_60_day[
                    (DateUtil.calculate_time_float(time, 60) > self.__macd_60_day['time']) & (
                            time <= self.__macd_60_day['time'])]['dif'].iloc[0] > 0:
                    print(f'{time} should sell5, but macd_60_day')
                    self.__change_mode(mode_day_60min_sell)
                    return
                else:
                    self.__trader.sell(self.__stock_id, day, time, price, 'sell5')

    def __day_60min_sell(self, day, time, price):
        """
        信号二的升级60分钟卖点方案：如果15分钟把60分钟带上0轴，则改看60分钟信号。即：15分钟买出信号出现时，60分钟MACD在0轴以下，15分钟卖出信号时，60分钟MACD在0轴以上了
        变更卖出条件为：【60分钟即将死叉，15分钟顶背离】（只要2个小时内两个条件都出现即可）。最后，则【60分钟死叉】一定卖出。
        :param day:
        :param time:
        :return:
        """
        # 正常卖出条件
        dead_cross_soon_60 = LineCrossService.filter_dead_cross_soon(self.__line_cross_soon_60)['time'].unique()
        top_deviation_15 = DeviationService.filter_macd_top_deviation(self.__macd_deviation_15)['time'].unique()
        dead_cross_60 = LineCrossService.filter_dead_cross(self.__line_cross_60)['time'].unique()
        origin_mode = self.__mode
        # 【60分钟即将死叉】
        if time in dead_cross_soon_60:
            func = lambda: self.__day_60min_sell_func(day, time, price)
            self.__delay_judge_point(occurrence_time_60_dead_soon, occurrence_time_15_top_deviation, time, 120, func)
            if not origin_mode == self.__mode:
                return
        # 【15分钟顶背离】
        if time in top_deviation_15:
            func = lambda: self.__day_60min_sell_func(day, time, price)
            self.__delay_judge_point(occurrence_time_15_top_deviation, occurrence_time_60_dead_soon, time, 120, func)
            if not origin_mode == self.__mode:
                return
        # 【60分钟死叉】一定卖出
        if time in dead_cross_60:
            self.__trader.sell(self.__stock_id, day, time, price, 'sell7')
            self.__change_mode(mode_day_15min_sell)
            return

    def __day_60min_sell_func(self, day, time, price):
        """
        执行60分钟卖出命令+切换模式的函数
        :param day:
        :param time:
        :param price:
        :return:
        """
        self.__trader.sell(self.__stock_id, day, time, price, 'sell6')
        self.__change_mode(mode_day_15min_sell)
