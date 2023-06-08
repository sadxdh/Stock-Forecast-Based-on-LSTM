# -*- coding:utf-8 -*-

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

# 准备数据集
data = pd.DataFrame({
    'text': [
        '这是一个正面的文本',
        '这是一个负面的文本',
        '这是一个中性的文本',
        '这是另一个正面的文本',
        '这是另一个负面的文本'
    ],
    'label': ['positive', 'negative', 'neutral', 'positive', 'negative']
})

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size=0.2, random_state=42)

# 特征提取
vectorizer = CountVectorizer()
X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)

# 训练模型
classifier = svm.SVC()
classifier.fit(X_train_vectors, y_train)

# 预测测试集
y_pred = classifier.predict(X_test_vectors)

# 输出预测结果
for text, true_label, pred_label in zip(X_test, y_test, y_pred):
    print(f"文本: {text}")
    print(f"真实标签: {true_label}")
    print(f"预测标签: {pred_label}")
    print()

