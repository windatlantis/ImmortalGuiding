
yymmdd = '%Y-%m-%d'
yymmdd_hhmmss = '%Y-%m-%d %H:%M:%S'
yymmdd_hhmmss_long = '%Y%m%d%H%M%S'

def format_yymmdd(time):
    return time.strftime(yymmdd)


def format_yymmdd_hhmmss(time):
    return time.strftime(yymmdd_hhmmss)


def format_yymmdd_hhmmss_long(time):
    return time.strftime(yymmdd_hhmmss_long)
