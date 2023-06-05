import pandas as pd
import matplotlib.pyplot as plt


class Resampling:
    def __init__(self, filename):
        self.filename = filename
        self.stock_week = None
        self.stock_train = None
        self.data = pd.read_csv(f"data\\{self.filename}.csv", index_col=0, parse_dates=[0])
        print("已读取到数据", self.data)
        self.resamplingWeek()
        self.draw()

    def resamplingWeek(self):
        self.stock_week = self.data['close'].resample('W').mean()
        print("按周重采样", self.stock_week)
        self.stock_train = self.stock_week[:'2019'].dropna()
        print("设置训练集", self.stock_train)
        self.stock_test = self.stock_week['2020':].dropna()
        print("设置测试集", self.stock_test)

    def draw(self):
        self.stock_train.plot()
        plt.title("stock_train")
        plt.show()
        self.stock_test.plot()
        plt.title("stock_test")
        plt.show()


if __name__ == '__main__':
    filename = "海康威视2010-05-05"
    data = Resampling(filename)
    stock_train = data.stock_train
    stock_test = data.stock_test
