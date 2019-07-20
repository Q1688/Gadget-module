#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : lianggq
# @Time  : 2019/7/19 20:17
# @FileName: logger.py
import os
import sys
import logging
import logging.handlers
import colorlog


class Logger(logging.Logger):
    def __init__(self):
        # 是否在终端中使用带色日志进行区别
        use_color = True
        # 模块名称
        logger_name = os.getcwd().split('\\')[-1]
        # 日志等级
        level = logging.INFO
        # 日志文件名
        logger_file = './log/%s' % logger_name + '_log.log'

        # 创建日志文件
        logging.Logger.__init__(self, logger_file)
        try:
            os.makedirs(os.path.dirname(logger_file))
        except FileExistsError:
            pass
        except FileNotFoundError:
            pass

        # 规定日志格式内容：
        log_format = logging.Formatter("[%(asctime)s] [" + logger_name
                                       + "] [%(levelname)s] %(filename)s [line:%(lineno)d] %(message)s")

        if not sys.stdout.isatty():
            # 判断执行输出流是否是终端，是终端直接显示日志
            try:
                if use_color:
                    log_colors = {
                        'DEBUG': 'green',
                        'INFO': 'blue',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'bold_red',
                    }

                    log_style = "%(log_color)s [%(asctime)s] [" + logger_name + \
                                "] [%(levelname)s] %(filename)s [line:%(lineno)d] %(message)s %(reset)s"

                    log_format = colorlog.ColoredFormatter(fmt=log_style, log_colors=log_colors, reset=True)
                    console_handle = logging.StreamHandler(sys.stdout)
                    console_handle.setLevel(level)
                    console_handle.setFormatter(log_format)
                    self.addHandler(console_handle)
                else:
                    file_handle = logging.StreamHandler(sys.stdout)
                    file_handle.setLevel(level)
                    file_handle.setFormatter(log_format)
                    self.addHandler(file_handle)
            except Exception as reason:
                self.error("%s" % reason)

        # 设置日志记录的大小和备份
        try:
            handler = logging.handlers.RotatingFileHandler(
                filename=logger_file,
                maxBytes=30 * 1024 * 1024,
                backupCount=1,
                mode='a',
                encoding=None,
                delay=0
            )
            handler.setLevel(level)
            handler.setFormatter(log_format)
            self.addHandler(handler)
        except Exception as reason:
            self.error("%s" % reason)


logger = Logger()
