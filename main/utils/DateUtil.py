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


def get_date_range(day_str, addition):
    days = []
    day = str2day(day_str)
    if addition > 0:
        days.append(day_str)
        for i in range(addition):
            days.append(day2str(day + dt.timedelta(days=i + 1)))
    else:
        for i in range(addition, 0):
            days.append(day2str(day + dt.timedelta(days=i)))
        days.append(day_str)
    return days
