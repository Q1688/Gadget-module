#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : lianggq
# @Time  : 2019/7/8 18:40
# @FileName: word_cloud.py
from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open('./A_father_love.txt', encoding='utf-8') as r:
    text = r.read()

# 词云背景图片的读取
b_back = plt.imread('./bilinear.jpg')

wordclouds = WordCloud(  # 此处不需要设置字体，因为默认的是英文
    width=800,
    height=400,
    mask=b_back,  # 若不选取背景图片可以设置为None
    scale=3,  # 字数频率少于3次的不显示
).generate(text)  # generate()从文本生成wordcloud

# plt.imshow()函数负责对图像进行处理，并显示其格式,interpolation设置了边界的模糊度或图片的模糊度
plt.imshow(wordclouds, interpolation='None')
# 关闭轴线和标签,若不关闭则写范围
plt.axis('off')
# plt.show()是将plt.imshow()处理后的函数显示出来
plt.show()
# 保存图片
wordclouds.to_file('result.jpg')
