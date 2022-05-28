import datetime as dt
from datetime import datetime, time

yymmdd = '%Y-%m-%d'
yymmdd_hhmmss = '%Y-%m-%d %H:%M:%S'
yymmdd_hhmmss_long = '%Y%m%d%H%M%S'
morning_start = time(9, 30, 0)
morning_end = time(11, 30, 0)
afternoon_start = time(13, 0, 0)
afternoon_end = time(15, 0, 0)


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


def time2date(time_float):
    time_float = int(time_float / 1000)
    return str2day(str(time_float), yymmdd_hhmmss_long)


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


def calculate_time_float(time_float, adjust_min):
    """
    时间运算
    :param time_float:
    :param adjust_min
    :return:
    """
    date_time = time2date(time_float)
    date_time = calculate_time(date_time, adjust_min)
    return int(day2str(date_time, yymmdd_hhmmss_long)) * 1000


def calculate_time(date_time, adjust_min):
    """
    时间运算
    :param date_time:
    :param adjust_min:
    :return:
    """
    date_time = date_time + dt.timedelta(minutes=adjust_min)
    date = date_time.date()
    if date_time.time() < morning_start:
        delta = date_time - datetime(year=date.year, month=date.month, day=date.day,
                                     hour=morning_start.hour, minute=morning_start.minute, second=morning_start.second)
        yesterday = date_time.date() + dt.timedelta(days=-1)
        yesterday = datetime(year=yesterday.year, month=yesterday.month, day=yesterday.day,
                             hour=afternoon_end.hour, minute=afternoon_end.minute, second=afternoon_end.second)
        return calculate_time(yesterday, delta.seconds / 60)
    elif morning_end < date_time.time() < afternoon_start:
        delta = date_time - datetime(year=date.year, month=date.month, day=date.day,
                                     hour=morning_end.hour, minute=morning_end.minute, second=morning_end.second)
        today = datetime(year=date.year, month=date.month, day=date.day,
                         hour=afternoon_start.hour, minute=afternoon_start.minute, second=afternoon_start.second)
        return calculate_time(today, delta.seconds / 60)
    elif date_time.time() > afternoon_end:
        delta = date_time - datetime(year=date.year, month=date.month, day=date.day,
                                     hour=afternoon_end.hour, minute=afternoon_end.minute, second=afternoon_end.second)
        tomorrow = date_time.date() + dt.timedelta(days=1)
        tomorrow = datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day,
                            hour=morning_start.hour, minute=morning_start.minute, second=morning_start.second)
        return calculate_time(tomorrow, delta.seconds / 60)
    return date_time


def between_minutes(time1, time2, trade_date):
    date1 = time2date(time1)
    date2 = time2date(time2)
    start = date1 if date1 < date2 else date2
    end = date2 if date1 < date2 else date1
    delta = end - start
    if delta.days > 0:
        count = 0
        count = count + between_minutes_in_one_day(start, datetime(year=start.year, month=start.month, day=start.day,
                                                                   hour=afternoon_end.hour, minute=afternoon_end.minute,
                                                                   second=afternoon_end.second))
        count = count + between_minutes_in_one_day(datetime(year=end.year, month=end.month, day=end.day,
                                                            hour=morning_start.hour, minute=morning_start.minute,
                                                            second=morning_start.second), end)
        if delta.days > 2:
            for i in range(1, delta.days - 1):
                day = start + dt.timedelta(days=i)
                if day in trade_date:
                    count = count + 4 * 60
        return count
    else:
        return between_minutes_in_one_day(date1, date2)


def between_minutes_in_one_day(date_time1, date_time2):
    start = date_time1 if date_time1 < date_time2 else date_time2
    end = date_time2 if date_time1 < date_time2 else date_time1
    delta = end - start
    if (start.time() < morning_end and end.time() < morning_end) or (
            start.time() > afternoon_start and end.time() < afternoon_end):
        return delta.seconds / 60
    else:
        return delta.seconds / 60 - 90
