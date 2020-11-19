# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : RegularFiltering.py
@Author: v_yanqyu
@Desc  : 正则表达过滤关键字段
@Date  : 2020/10/16 17:07
'''

from Logger.GlobalLog import  Logger # 导入日志模块
from Utils.DictClean import YamlHandle
logger = Logger.write_log()#调用日志模块

print(YamlHandle.filterkey(filepath=r'..\Config\WhiteActivity.txt', keyword='com.tencent.now',
                           target='..\Result\ActivityTemp'))

