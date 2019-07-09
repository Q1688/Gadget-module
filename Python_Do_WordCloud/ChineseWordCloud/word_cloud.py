#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : lianggq
# @Time  : 2019/7/8 23:35
# @FileName: word_cloud.py
import jieba
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

with open('./假如给我三天光明.txt', encoding='utf-8') as r:
    text = r.read()
    # print(text)
    textcut = ' '.join(jieba.cut(text))
    # print(textcut)

b_img = plt.imread('./test.png')
wordcloubs = WordCloud(
    font_path='C:/Windows/Fonts/MSYH.TTC',  # 设定文字的类型为中文黑体。
    width=800,
    height=400,
    mask=b_img,  # 若不选取背景图片可以设置为None
    scale=2,  # 字数频率少于3次的不显示
).generate(textcut)

plt.imshow(wordcloubs, interpolation='None')
plt.axis('off')
plt.show()
wordcloubs.to_file('result.jpg')
