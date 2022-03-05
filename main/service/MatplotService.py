# -*- coding:utf-8 -*-
"""
@Time : 2022/3/5 10:44
@Author: windatlantis
@File : MatplotService.py
"""

import matplotlib.pyplot as plt


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


def show(data, title, xlabel):
    plt.plot(data)
    plt.title(title, fontsize=15)
    plt.xlabel(xlabel, fontsize=15)
    plt.show()

