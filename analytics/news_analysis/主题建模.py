# -*- coding:utf-8 -*-

import gensim
from gensim import corpora

# 准备文档集合
documents = [
    "23Q1 业绩承压，毛利率开始回升。",
    "企业数字化需求引领BG 业务增长。",
    "持续加大AI 投入，形成AI 技术积累。",
    "盈利预测与投资建议。",
]

# 分词处理
tokenized_documents = [document.split() for document in documents]

# 创建词典
dictionary = corpora.Dictionary(tokenized_documents)

# 创建文档-词频矩阵
corpus = [dictionary.doc2bow(document) for document in tokenized_documents]

# 构建LDA模型
lda_model = gensim.models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=2, passes=10)

# 打印每个主题的关键词
for topic_id, topic_keywords in lda_model.print_topics():
    print(f"Topic {topic_id + 1}: {topic_keywords}")
