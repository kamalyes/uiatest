#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
@File  :InspectCrawling.py
@Author:v_yanqyu
@Desc  :检查页面是否支持爬取
@Date  :2020/9/25-20:15
'''
import requests
from Logger import GlobalLog
logger = GlobalLog.Logger().write_log()  #导入日志模块