#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
# FileName： ReadConfig.py
# Author : v_yanqyu
# Desc: PyCharm
# Date： 2020/9/6 15:55
'''
__author__ = 'v_yanqyu'
from configobj import ConfigObj

conf_ini = "../Config/Logger.ini"
config = ConfigObj(conf_ini, encoding='UTF8')

# 读配置文件
print(config['Apk_Info'])