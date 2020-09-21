#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
# FileName： ImportJar.py
# Author : v_yanqyu
# Desc: PyCharm
# Date： 2020/6/25 19:55
'''
__author__ = 'v_yanqyu'

from Logger import GlobalLog  # 导入日志模块
logger = GlobalLog.Logger.write_log() #调用日志模块
# 导入所需要的第三方库
def check_import():
    try:
        import os, sys, xlrd, xlwt, json,datetime
        logger.info("所需模块导入成功 Required modules imported successfully！")
    except Exception as ImportError:
        logger.error("本地环境没有所需第三方库 Check whether the third-party library of the local environment is downloaded")
