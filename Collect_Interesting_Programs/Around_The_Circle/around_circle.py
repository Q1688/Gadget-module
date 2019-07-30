#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : lianggq
# @Time  : 2019/7/30 17:06
# @FileName: around_circle.py

def circle(size):
    # 二维数组
    array = [[0] * size]

    # 构建七行七列的二维数组
    for i in range(size - 1):
        array += [[0] * size]

    # 该orient代表绕圈的方向
    # 其中0代表向下，1代表向右，2代表向左，3代表向上
    orient = 0
    # 行数
    j = 0
    # 列数
    k = 0

    for i in range(1, size * size + 1):
        array[j][k] = i
        if j + k == size - 1:
            if j > k:
                orient = 1
            else:
                orient = 2

        elif (k == j) and (k >= size / 2):
            orient = 3
        elif (j == k - 1) and (k <= size / 2):
            orient = 0

        if orient == 0:
            j += 1
        elif orient == 1:
            k += 1
        elif orient == 2:
            k -= 1
        elif orient == 3:
            j -= 1

    for i in range(size):
        for j in range(size):
            print('%02d ' % array[i][j], end="")
        print("")


if __name__ == '__main__':
    circle(7)