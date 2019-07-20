#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : lianggq
# @Time  : 2019/7/20 17:37
# @FileName: test.py

from Fog_Record.logger import logger

if __name__ == '__main__':
    a = 0
    b = 10
    try:
        consult = b / a
        print(consult)
    except Exception as reson:
        logger.error(reson)
