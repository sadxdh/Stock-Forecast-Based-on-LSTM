
import tushare as ts

#查询当前所有正常上市交易的股票列表

data = ts.stock_basic()
print(data)
