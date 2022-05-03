"""
baostock变量
"""

# fields：指示简称，支持多指标输入，以半角逗号分隔，填写内容作为返回类型的列。
fields = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"
fields_min = "date,time,code,open,high,low,close,volume,amount,adjustflag"

# frequency：数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写；
# 指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
frequency = ["d", "w", "m"]
frequency_min = ["5", "15", "30", "60"]

# adjustflag：复权类型，默认不复权：3；1：后复权；2：前复权。已支持分钟线、日线、周线、月线前后复权。 BaoStock提供的是涨跌幅复权算法复权因子
adjustflag = ["1", "2", '3']

