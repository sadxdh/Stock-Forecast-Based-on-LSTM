import pandas as pd
import os
import re
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import jieba
import thulac
from concurrent.futures import ProcessPoolExecutor

stockname = '上海临港'
path = 'data/news_data/'  # 右侧要有‘/’

def readCSV(file):
    report_df = pd.read_csv(os.path.join(path, file), names=['title', 'institution_type', 'institution_name', 'author', 'date', 'content'])
    report_df.set_index(report_df['date'], inplace=True)
    report_df.sort_index(inplace=True)  # 排序后生效，改变原数据
    report_df.drop(report_df['date'])
    return report_df

def coarseWords(report_df):
    def func(x):
        # 去除标点符号
        cleaned_text = re.sub(r'[^\u4e00-\u9fa5]+', '', x)
        # 转换为小写
        cleaned_text = cleaned_text.lower()
        # 分词
        tokens = jieba.cut(cleaned_text)
        # 去除停用词
        stop_words = set(stopwords.words('chinese'))
        filtered_tokens = [token for token in tokens if token not in stop_words]
        # print(len(filtered_tokens))
        # 输出处理后的文本
        cleaned_text = ' '.join(filtered_tokens)
        # print(cleaned_text)
        return cleaned_text
    report_df['coarseWords'] = report_df['content'].apply(func)
    return report_df

def thinWords(report_df):
    def func(x):
        thu1 = thulac.thulac(filt=True)  # 词性标注
        df = pd.DataFrame(thu1.cut(x), columns=['word', 'counts'])
        word_count = df[df['counts'] == 'v'].groupby('word').count()
        word_count_list = word_count.to_records().tolist()
        # print(word_count_list)
        return word_count_list
    report_df['thinWords'] = report_df['coarseWords'].apply(func)
    return report_df

def keyWords(report_df):
    def func(x):
        import jieba.analyse
        keywords = jieba.analyse.extract_tags(x, topK=10, withWeight=True)
        print(keywords)
        return keywords
    report_df['keyWords'] = report_df['content'].apply(func)
    return report_df

def affectiveClassification(report_df):
    def func(x):
        # 创建情感分析器
        sia = SentimentIntensityAnalyzer()
        # 对文本进行分词
        words = jieba.lcut(x)
        # 对每个分词进行情感分析
        sentiments = []
        for word in words:
            sentiment_scores = sia.polarity_scores(word)
            sentiments.append(sentiment_scores['compound'])
        # 计算情感得分
        sentiment_score = sum(sentiments) / len(sentiments)
        # 输出情感分类结果
        if sentiment_score > 0:
            return 'positive'
        elif sentiment_score < 0:
            return 'negative'
        else:
            return 'neutral'
    report_df['affectiveClassification'] = report_df['content'].apply(func)
    return report_df

def multi_process():
    files = [file for file in os.listdir(path) if re.match(rf'{stockname}研究报告.*\.csv', file)]
    print(files)
    with ProcessPoolExecutor() as pool:
        pool.map(report_auto_process, files)

# cpu密集型，使用多进程加速
def report_auto_process(file):
    report_df = readCSV(file)
    report_df = coarseWords(report_df)
    report_df = thinWords(report_df)
    report_df = keyWords(report_df)
    report_df = affectiveClassification(report_df)
    print(report_df.columns)
    # file = ‘海康威视研究报告第1页.csv’ 保存文件名为：海康威视研究报告第1页_processed.csv
    savefilename = path + file.split('.')[0]+'_processed.'+file.split('.')[1]
    print(savefilename)
    report_df.to_csv(savefilename, encoding="utf_8_sig")

def save_total(report_df):
    report_df.to_csv(f'{path}/{stockname}_report_total.csv', encoding="utf_8_sig")
    print(report_df)

def concatCSV():
    report_df = pd.DataFrame()
    files = [file for file in os.listdir(path) if re.match(rf'{stockname}研究报告.*\.csv', file)]
    for file in files:
        if re.match(rf'{stockname}研究报告.*_processed\.csv', file):
            report_df = pd.concat([report_df, pd.read_csv(os.path.join(path, file))], axis=0)
    save_total(report_df)
    return report_df

def main():
    multi_process()
    concatCSV()

if __name__ == '__main__':
    main()
    # import nltk
    # nltk.download('vader_lexicon')
    # nltk.download('stopwords')
    # nltk.download('punkt')