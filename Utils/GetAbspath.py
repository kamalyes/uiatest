#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
# FileName： GetAbspath.py
# Author : v_yanqyu
# Desc: PyCharm
# Date： 2020/5/6 19:15
'''
__author__ = 'v_yanqyu'
import os
from Logger import GlobalLog
logger = GlobalLog.Logger.write_log()
# 获取当前目录
def get_pwd():
    # print (os.getcwd())
    pwd = os.path.abspath(os.path.dirname(__file__))
    # logger.info ('获取到当前目录：{}'.format(pwd))
    return pwd

# 获取上级目录
def get_superiordirectory():
    superiordirectory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # logger.info ('获取上级目录：{}'.format(superiordirectory))
    return superiordirectory
    # print (os.path.abspath(os.path.dirname(os.getcwd())))
    # print (os.path.abspath(os.path.join(os.getcwd(), "..")))

# 获取上上级目录
def get_superiordirectorys():
    superiordirectorys = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    # logger.info ('获取上上级目录：{}'.format(superiordirectorys))
    return superiordirectorys

if __name__ == '__main__':
    get_pwd()
    get_superiordirectory()
    get_superiordirectorys()
