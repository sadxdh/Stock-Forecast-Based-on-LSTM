# 原著 https://www.mdpi.com/43264
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class PeakDetection:
    def __init__(self, filename):
        self.filename = filename
        self.stock_week = None
        self.stock_train = None
        self.data = pd.read_csv(f"data/stocks_data/{self.filename}.csv", index_col=0, parse_dates=[0])
        print("已读取到数据", self.data)
        self.vis()

    def AMPD(self, data):
        """
        实现AMPD算法
        :param data: 1-D numpy.ndarray
        :return: 波峰所在索引值的列表
        """
        p_data = np.zeros_like(data, dtype=np.int32)
        count = data.shape[0]
        arr_rowsum = []
        for k in range(1, count // 2 + 1):
            row_sum = 0
            for i in range(k, count - k):
                if data[i] > data[i - k] and data[i] > data[i + k]:
                    row_sum -= 1
            arr_rowsum.append(row_sum)
        min_index = np.argmin(arr_rowsum)
        max_window_length = min_index
        for k in range(1, max_window_length + 1):
            for i in range(k, count - k):
                if data[i] > data[i - k] and data[i] > data[i + k]:
                    p_data[i] += 1
        return np.where(p_data == max_window_length)[0]

    def sim_data(self):
        x = self.data.index
        y = self.data['close']
        # print("x:", x)
        # print("y:", y)
        return x, y

    def vis(self):
        x, y = self.sim_data()
        plt.plot(x, y)
        px = x[self.AMPD(y)]
        print("长度：", px)
        self.data_extreme_value = self.data.copy()
        self.data_extreme_value['mixumum'] = pd.Series([])
        self.data_extreme_value['mixumum'] = self.data.index.isin(px)


        px = x[self.AMPD(-y)]
        print("长度：", px)
        self.data_extreme_value = self.data_extreme_value.copy()
        self.data_extreme_value['minumum'] = pd.Series([])
        self.data_extreme_value['minumum'] = self.data.index.isin(px)

        self.data_extreme_value.to_csv(f'data/stocks_data/{self.filename}_MaxMin.csv')


if __name__ == '__main__':
    filename = "海康威视"
    P = PeakDetection(filename)
