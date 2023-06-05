# 先引入后面可能用到的包（package）
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
from pylab import mpl


class Kline:
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_csv(f"data\\{self.filename}.csv")
        self.df.index = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_index()
        self.kLine()
        self.draw()

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
    def kLine(self):
        types = ['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA',
                 'TRIMA', 'KAMA', 'MAMA', 'T3']
        self.df_ma = pd.DataFrame(self.df.close)
        for i in range(len(types)):
            self.df_ma[types[i]] = ta.MA(self.df.close, timeperiod=5, matype=i)
        print('上证指数各种类型移动平均线（近200个工作日）')
        print(self.df_ma.tail())

    def draw(self):
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False
        self.df_ma.iloc[:].plot(figsize=(16, 6))
        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        plt.title('上证指数各种类型移动平均线（近200个工作日）', fontsize=15)
        plt.xlabel('')
        plt.show()


if __name__ == '__main__':
    filename = '海康威视2010-05-05'
    Kline(filename)
