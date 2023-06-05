from analytics import Resampling
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.layers import LSTM
from keras.layers import Dense
from keras.models import Sequential
from sklearn.metrics import mean_squared_error
import numpy as np


class LSTMtrain:
    def __init__(self, stock_train, stock_test):
        self.stock_train = stock_train
        self.stock_test = stock_test
        self.scaler, train_scaled, test_scaled = self.scale()
        # 构建一个LSTM模型并训练，样本数为1，训练次数为3，LSTM层神经元个数为4


    def scale(self):
        # 创建一个缩放器，将数据集中的数据缩放到[-1,1]的取值范围中
        self.scaler = MinMaxScaler(feature_range=(-1, 1))
        # 使用数据来训练缩放器
        self.scaler = self.scaler.fit(self.stock_train)
        # 使用缩放器来将训练集和测试集进行缩放
        train_scaled = self.scaler.transform(self.stock_train)
        test_scaled = self.scaler.transform(self.stock_test)
        return self.scaler, train_scaled, test_scaled


if __name__ == '__main__':
    def getName(code, exchange):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42'
        }
        url = f'http://qt.gtimg.cn/q=s_{exchange}{code}'
        code_info_resp = requests.get(url, headers=headers)
        if code_info_resp.status_code == 200:
            print("股票名称查询成功")
        stocks_name = code_info_resp.text.split('~')[1] + start_time
        print(stocks_name)
        return stocks_name


    code = '002415'
    start_time = '2010-05-05'
    exchange = 'sz'
    stock_name = getName(code, exchange)
    data = Resampling.Resampling(stock_name)
    stock_train = data.stock_train
    stock_test = data.stock_test
    LSTMtrain(stock_train, stock_test)
