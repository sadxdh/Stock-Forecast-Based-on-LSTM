# -*- coding:utf-8 -*-
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# 准备数据集
dataset = [['牛奶', '面包', '尿布'],
           ['可乐', '面包', '尿布', '啤酒'],
           ['牛奶', '尿布', '啤酒', '鸡蛋'],
           ['面包', '牛奶', '尿布', '啤酒'],
           ['面包', '牛奶', '尿布', '可乐']]

# 转换数据集为二进制编码矩阵
te = TransactionEncoder()
te_array = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_array, columns=te.columns_)

# 找到频繁项集
frequent_itemsets = apriori(df, min_support=0.3, use_colnames=True)

# 根据频繁项集生成关联规则
association_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

# 输出结果
print("频繁项集:")
print(frequent_itemsets)
print("\n关联规则:")
print(association_rules)
