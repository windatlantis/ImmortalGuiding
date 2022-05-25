import datetime as dt
from datetime import datetime

yymmdd = '%Y-%m-%d'
yymmdd_hhmmss = '%Y-%m-%d %H:%M:%S'
yymmdd_hhmmss_long = '%Y%m%d%H%M%S'


def format_yymmdd(time):
    return time.strftime(yymmdd)


def format_yymmdd_hhmmss(time):
    return time.strftime(yymmdd_hhmmss)


def format_yymmdd_hhmmss_long(time):
    return time.strftime(yymmdd_hhmmss_long)


def day2str(day, format_str='%Y-%m-%d'):
    return datetime.strftime(day, format_str)


def str2day(day_str, format_str='%Y-%m-%d'):
    return datetime.strptime(day_str, format_str)


def get_date_range(day_str, n):
    """
    获取连续n+1天（算上day_str）
    :param day_str:
    :param n:为正时间向前，为负时间向后
    :return:
    """
    days = []
    day = str2day(day_str)
    if n > 0:
        days.append(day_str)
        for i in range(n):
            days.append(day2str(day + dt.timedelta(days=i + 1)))
    else:
        for i in range(n, 0):
            days.append(day2str(day + dt.timedelta(days=i)))
        days.append(day_str)
    return days


def calculate_time(time_int, adjust_min):
    """
    时间运算
    :param time_int:
    :param adjust_min
    :return:
    """
    time_int = int(time_int / 1000)
    time = str2day(str(time_int), yymmdd_hhmmss_long)
    time = time + dt.timedelta(minutes=adjust_min)
    return int(day2str(time, yymmdd_hhmmss_long)) * 1000
