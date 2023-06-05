import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.style as style


# 读取数据
def main(stock_name):
    df = pd.read_csv(f"../data/{stock_name}.csv")

    df.dropna(inplace=True)
    df = df.set_index(['date'])

    predict_count = int(len(df) * 0.02)
    df['label'] = df['close'].shift(-predict_count)
    print(df)

    X = df.drop(['code', 'label'], axis=1)
    y = df['label'][:-predict_count]

    scale = StandardScaler()
    scale.fit(X)
    x = scale.transform(X)
    # print(X)

    X_lately = X[-predict_count:]
    X = X[:-predict_count]

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.02)

    model = LinearRegression()
    model.fit(x_train, y_train)
    print(model.score(x_test, y_test))

    predict = model.predict(X_lately)
    print(predict)

    df['predict'] = np.nan
    print(df)

    # print(time.mktime(time.strptime(df.index[-1], "%Y-%m-%d")))
    last_date_st = time.mktime(time.strptime(df.index[-1], "%Y-%m-%d"))
    next_date_st = last_date_st + 86400
    # next_date = datetime.datetime.fromtimestamp(next_date_st)
    # print(next_date)

    for i in predict:
        next_date = datetime.datetime.fromtimestamp(next_date_st)
        df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]
        next_date_st += 86400

    print(df.tail(40))

    style.use('ggplot')
    # df['close'].plot()
    df['predict'].plot()
    plt.show()


if __name__ == '__main__':
    filename = "海康威视2010-05-05"
    main(filename)
