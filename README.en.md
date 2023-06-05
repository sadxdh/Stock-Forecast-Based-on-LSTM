# 股票分析（[新浪财经](https://finance.sina.com.cn/)）

## 最终目标

- 案例：海康威视（要求不仅仅适用于海康威视股票，同时可以实现其他股票一键预测）

1. 全自动化部分：数据获取，数据处理，数据分析，数据展示，数据格式化、模型训练、模型预测
2. 半自动化部分：模型选取（根据数据具体分布，提示模型选择）
3. 手动部分：股票选择，股票买卖（项目补充部分）

## 数据源

网页爬取，财经库

## 技术需求

Python基础，python分析（pandas，numpy），可视化（matplotlib），机器学习（sklearn）

## 项目结构（加粗为文件夹）

**data_collection**：存放数据获取脚本，包括新闻爬虫，股票获取脚本

1. **news_collection**：存放新闻爬虫脚本
   1. 要求：
      1. 脚本内包含可选参数：日期（从某日期起或特定某一天）
      2. 尽可能爬取足够多的股票分析报告
   2. 多种类新闻
2. **stocks_collection**：存放股票数据获取脚本
        3. 要求：
               1. 脚本内包含可选参数：日期，股票代码

**data**：存放所有的数据文件

1. **news_data**：新闻数据（txt文件，首行：标题、时间、来源/作者）
   1. **研究报告**--[研究报告|研究评级|机构研报_新浪财经_新浪网 (sina.com.cn)](https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=002415&t1=all)
   2. **大市评论**--[股市及时雨_证券_财经_新浪网 (sina.com.cn)](https://roll.finance.sina.com.cn/finance/zq1/gsjsy/index.shtml)
   3. **个股点评**--[个股点评_证券_新浪财经 (sina.com.cn)](http://finance.sina.com.cn/roll/index.d.html?cid=56588)
   4. **证券报**--[四大证券报精华_财经_新浪网 (sina.com.cn)](https://finance.sina.com.cn/focus/zqbjh/)
   5. **行业对比**--[行情中心_新浪财经_新浪网 (sina.com.cn)](https://vip.stock.finance.sina.com.cn/mkt/)
      1. 同板块股票各时期走势（可以调用股票分析模块（analytics））
2. **stocks_data**：股票数据
   1. 要求：
      1. csv文件，英文逗号分隔符，带表头
      2. 数据内容必须包括：‘date’（日期），‘close’（收盘价）

**analytics**：news文本处理和stocks数据处理

1.  **news_analysis**
2.  **stocks_analysis**

**gui**：GUI文件（项目补充部分）

**models**：保存训练好的model

**model_train**：保存机器学习训练脚本

**Visualization**：保存数据可视化文件（包括图表等）

## 项目主体实现步骤

1. 数据获取

   1. 股票数据
   2. 股票新闻数据

2. 数据分析

   1. 股票数据分析
      1. 基本数据处理
      2. 重采样等绘制基本图表
      3. 走势分析（单位时间内上升或下降比率）

   1. 股票新闻分析
      1. 词频统计（按时间统计各个时期出现次数较多的词、除杂）
      2. 按时间频率，分析出单位时间段内股票走势，计算出上涨或下跌幅度

3. 机器学习预测--通过模型提供预测对新增数据集提供发展趋势

   1. 模型构建（构建模型数据集）
   2. 训练模型
   3. 测试模型（原数据与预测对比）
   4. 模型调优（参数调优、模型替换等）
      1. 提供模型测试分数，挑出各项数据得分较高的模型


## 补充项目

网络编程：要求实现客户端与服务器交互
页面设计：终端界面设计（手机端或电脑端、服务器端）
项目架构：C/S

## 案例样本

### 网页样本数据

[数据中心 _ 东方财富网 (eastmoney.com)](https://data.eastmoney.com/center/)


## 技术教程

### 数据集样本：

[农业银行 2.85 (1.06%) (601288)_个股行情_网易财经 (163.com)](http://quotes.money.163.com/trade/cjmx_601288.html)

 

### Python基础

[Python基础教程，Python入门教程（非常详细） (biancheng.net)](http://c.biancheng.net/python/)



### 机器学习

[吴孟达_coursera_machine-learning_无字幕无翻译](https://www.coursera.org/learn/machine-learning)

[吴孟达bilibili_machine-learning中英字幕](https://www.bilibili.com/video/BV1Pa411X76s)