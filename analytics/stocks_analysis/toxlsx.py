import pandas as pd


class toxlsx:
    def __init__(self, filename):
        self.filename = filename
        self.stock_week = None
        self.stock_train = None
        self.data = pd.read_csv(f"..\\data\\{self.filename}.csv", index_col=0, parse_dates=[0])
        self.data.to_excel(f"..\\data\\{self.filename}.xlsx")


if __name__ == '__main__':
    filename = "海康威视2010-05-05"
    data = toxlsx(filename)
