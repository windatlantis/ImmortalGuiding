# -*- coding:utf-8 -*-
"""
@Time : 2022/3/5 10:43
@Author: windatlantis
@File : DrawPic.py
"""

from main.domain import DataCreator
from main.service import MatplotService


def draw_macd_pic(stock_id, read_csv=True):
    """
    绘制macd图
    :param stock_id:
    :param read_csv:
    :return:
    """
    df_macd, df_macd_data = DataCreator.get_stock_n_year_macd(stock_id, 1, read_csv)
    MatplotService.init_plt_style()
    # 绘制图片
    MatplotService.show(df_macd, title=stock_id + '近1年macd', xlabel='时间', legends=['dif', 'dea', 'macd'])
