# -*- coding:utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# 原始文本
text = """
23Q1 业绩承压，毛利率开始回升。根据公司23 年一季报，公司实现营收162.01 亿元；同比下降1.94%；实现归母净利润18.11 亿元，同比下降20.69%，营收与归母净利润的下降趋势均较22 年Q4 有所缓和。23 年Q1公司毛利率为45.17%，较22 年的42.29%有所回升。受政治因素、通胀等方面影响，海外市场整体出现负增长，但部分发展中国家需求情况尚可。我们认为，公司注重营收质量，虽然公司短期业绩有所下滑，但已经有明显的转好趋势，2023 年有望实现营收和净利润的较快增长。
企业数字化需求引领BG 业务增长。企业数字化转型的势头较好，公司EBG业务已率先恢复正增长。由于公司的SMBG 业务主要针对于小商户、小工厂、小企业、小单位，在经济复苏的背景下，SMBG 业务决策链较短，餐饮旅游的恢复增长将直观带动业务的增长，EBG、PBG 业务将随后逐步恢复，恢复速度相对较慢。我们认为，SMBG 业务的恢复将逐步带动公司业绩回暖，EBG和PBG 的业务业绩的逐步回升将为公司的营收和净利润带来进一步的增长。
持续加大AI 投入，形成AI 技术积累。公司较早地对人工智能的技术趋势作出反应，在技术上实现了更大规模和更深的网络、更强的并行能力、更强的数据中心、更强的数据生成和数据标注的能力。在AI 技术的发展过程中，公司的AI 模型规模持续扩大，已形成了千卡并行的能力并训练了百亿级参数的模型。公司始终专注于AIOT，从客户的场景需求出发解决问题。我们认为，公司较早地专注AIOT，在技术上已有一定的积累，未来能够更好地实现AI技术地产品化和落地。
盈利预测与投资建议。我们预计，公司2023/2024/2025 年EPS 分别为1.78/2.11/2.49 元。海康威视作为智能物联龙头企业，在行业中具有较为明显的优势竞争优势地位，我们给予海康威视2023 年25-30 倍PE，对应6 个月合理价值区间为44.50-53.40 元，维持“优于大市”评级。
风险提示：行业需求不及预期，市场竞争加剧的风险。
"""

# 创建TF-IDF向量化器
vectorizer = TfidfVectorizer()

# 对文本进行向量化
tfidf_matrix = vectorizer.fit_transform([text])

# 获取词汇表
vocabulary = vectorizer.get_feature_names()

# 提取关键词及对应的权重
keywords = []
weights = []
for i in tfidf_matrix.nonzero()[1]:
    keywords.append(vocabulary[i])
    weights.append(tfidf_matrix[0, i])

# 将关键词和权重组成数据框
keywords_df = pd.DataFrame({'Keyword': keywords, 'Weight': weights}).sort_values(by='Weight', ascending=False)

# 输出关键词及对应的权重
print(keywords_df)
