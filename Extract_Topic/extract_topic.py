#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : lianggq
# @Time  : 2019/7/10 17:08
# @FileName: extract_topic.py
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# 定义列表存放清洗后的
lists = []
with open('./datas/data.txt', encoding='utf-8') as r:
    readlines = r.readlines()
    for line in readlines:
        word = jieba.cut(line)
        for i in word:
            lists.append(i)

# 从文件导入停用词表
with open('./StopWords/中文停用词库.txt', encoding='utf-8') as fp:
    stopword = fp.read()
stop_list = stopword.splitlines()

# 创建词袋
word_vec = TfidfVectorizer(stop_words=stop_list)
tf = word_vec.fit_transform(lists)

# 文本转化为特征向量
centor = tf.toarray()
# 使用LDA方法指定主题
model = LatentDirichletAllocation(n_topics=1,
                                  max_iter=50,
                                  learning_method='online',
                                  learning_offset=50,
                                  random_state=0,
                                  )
# 训练模型
model.fit(tf)
# 有关主题词语的个数
n_top_words = 10


# 把主题里面的前若干个关键词显示出来
def top_words(model, feature_name, n_top_words):
    for topic_id, topic in enumerate(model.components_):
        print('Topic个数: %d' % topic_id)
        print(' '.join([feature_name[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))


# 获取除停用词之后的所有文本的词汇
words = word_vec.get_feature_names()

if __name__ == '__main__':
    # # 获取除停用词之后的所有文本的词汇
    # print(words)
    # # 获取除停用词之后的所有文本的词汇和频率
    # print(word_vec.vocabulary_)
    # print(lda)
    top_words(model, words, n_top_words)
