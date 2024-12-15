# 示例调用

#重要：：：token必须设置：：：
from chinamindata.c_min import set_token
set_token('637de0f1570f7273a634df8988be469a59')


#1可以获取大A股票分钟，freq取值1min'、'5min'、'15min'、'30min'、'60min'
from chinamindata.china_min import get_min_data
df = get_min_data( code = '000001.SZ', start_date = '2024-07-07 09:00:00',
                       end_date = '2024-07-22 15:00:00',freq='60min',)
print(df)

#2可以获取大A股票分钟开盘竞价
from chinamindata.china_min_open import get_open_data
df = get_open_data(trade_date='20241122')
print(df)

#3可以获取大A股票分钟闭盘竞价
from chinamindata.china_min_close import get_close_data
df = get_close_data(trade_date='20241122')
print(df)


#4可以获取大A股票、指数、基金的列表
from chinamindata.china_list import get_list
df = get_list(type="stock")
print(df)