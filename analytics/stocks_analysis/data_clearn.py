import pandas as pd
import talib as ta
from PeakDetection import PeakDetection

def main(filename):
    df = pd.read_csv(f"data/stocks_data/{filename}.csv")
    # df.index = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # # 假设您已经有了一个名为df的DataFrame对象，其中包含日期（在df.index中）和收盘价（在df['close']中）
    # # 创建新列来存储五日均线和十日均线
    df['5日均线'] = ta.SMA(df['close'], timeperiod=5)
    df['10日均线'] = ta.SMA(df['close'], timeperiod=10)

    # # 假设您已经有了一个名为df的DataFrame对象，其中包含日期（在df.index中）和收盘价（在df['close']中）
    # # 创建新列来存储涨跌幅度
    # df = df.tail(100)
    df['涨幅'] = (df['close'] - df['close'].shift(5)) / df['close'].shift(5)
    df['跌幅'] = (df['close'].shift(5) - df['close']) / df['close'].shift(5)
    clean_filename = f'{filename}_clean'
    filename = f'data/stocks_data/{clean_filename}.csv'
    df.to_csv(filename)
    return clean_filename


if __name__ == '__main__':
    f = open('target', 'r', encoding='utf-8')
    stock_name = f.read().split('\n')
    print(stock_name)
    for s in stock_name:
        stock = s.split('（')[0]
        print(stock)
        clean_filename = main(stock)
        P = PeakDetection(clean_filename)


'''
    SMA：简单移动平均，简单的按照一定的周期计算出的移动平均线。
    EMA：指数移动平均，根据某一特定的指数来计算出的移动平均线。
    WMA：加权移动平均，把更新的数据赋予更多的权重，使其在计算移动平均线时，具有更大的影响力。
    DEMA：双指数移动平均，是对EMA的一种改进，它以某种方式抵消了EMA所产生的滞后性。
    TEMA：三指数移动平均，是对DEMA的一种改进，其计算公式与DEMA基本相同，只是改变了加权因子。
    TRIMA：三角形移动平均，与EMA相比，它更加均衡地分配权重，使得计算更加精准。
    KAMA：考夫曼自适应移动平均，基于市场变化的持续性和变化的速度，自适应地调整自身的参数。
    MAMA：MESA自适应移动平均，是一种强大的自适应移动平均，使用不同的周期来处理市场中的趋势和波动。
    T3：拓展三指数移动平均，是对TEMA的一种改进，它使用一个额外的因子来调整移动平均线的反应速度。
'''
