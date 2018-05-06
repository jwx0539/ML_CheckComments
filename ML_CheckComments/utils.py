import pandas as pd
import numpy as np
import config
import os
import re
import jieba.posseg as pseg
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


def prepare_data():
    df_movie = pd.read_csv('./output/movie_comments.csv',encoding='GB18030')
    #print(df_movie[:10])
    #添加标签
    df_movie['label'] = df_movie['分数'].map(config.text_type_dic)
    #文本处理
    df_movie['proc_text'] = df_movie['影评'].apply(preprocess_text)
    #保存结果
    df_movie.to_csv(os.path.join(config.output_path,'new_comments.csv'),encoding="GB18030")
    #数据集划分
    train_data, test_data = train_test_split(df_movie, test_size=1/4, random_state=0)
    return train_data, test_data

def preprocess_text(raw_text):
    # 加载停用词表
    stop_words_path = './stop_words/'
    stopwords1 = [line.rstrip() for line in open(os.path.join(stop_words_path, '中文停用词库.txt'), 'r', encoding='utf-8')]
    stopwords2 = [line.rstrip() for line in open(os.path.join(stop_words_path, '哈工大停用词表.txt'), 'r', encoding='utf-8')]
    stopwords3 = [line.rstrip() for line in open(os.path.join(stop_words_path, '四川大学机器智能实验室停用词库.txt'), 'r', encoding='utf-8')]
    stopwords = stopwords1 + stopwords2 + stopwords3

     # 1. 使用正则表达式去除非中文字符
    filter_pattern = re.compile('[^\u4E00-\u9FD5]+')
    chinese_only = filter_pattern.sub('',raw_text)
    # 2. 结巴分词+词性标注
    word_list = pseg.cut(chinese_only)
    # 3. 去除停用词，保留有意义的词性
    # 动词，形容词，副词
    used_flags = ['v', 'a', 'ad']
    meaninful_words = []
    for word, flag in word_list:
        if (word not in stopwords) and (flag in used_flags):
            meaninful_words.append(word)
    return ' '.join(meaninful_words)

def feature_engineering(train_data,test_data):
    train_proc_text = train_data['proc_text'].values
    test_proc_text = test_data['proc_text'].values

    #TF-IDF特征提取
    tfidf_vectorizer = TfidfVectorizer()
    train_tfidf_feat = tfidf_vectorizer.fit_transform(train_proc_text).toarray()
    test_tfidf_feat = tfidf_vectorizer.transform(test_proc_text).toarray()

    # 词袋模型
    count_vectorizer = CountVectorizer()
    train_count_feat = count_vectorizer.fit_transform(train_proc_text).toarray()
    testcount_feat = count_vectorizer.transform(test_proc_text).toarray()

    #合并特征
    train_X = np.hstack((train_tfidf_feat,train_count_feat))
    test_X = np.hstack((test_tfidf_feat,testcount_feat))
    return train_X,test_X



if __name__ == '__main__':
    feature_engineering()



