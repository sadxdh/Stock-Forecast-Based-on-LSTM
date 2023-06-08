import pandas as pd
import os
import re

path = 'data//news_data'
files = os.listdir(path)

stockname = '海康威视'
report_df = pd.DataFrame()
for file in files:
    if re.match(rf'{stockname}研究报告.*\.csv', file):
        report_df = pd.concat([report_df, pd.read_csv(os.path.join(path, file))], ignore_index=True)

report_df.to_csv('report_total.csv')
print(report_df)
