# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : ReadDatas.py
@Author: v_yanqyu
@Desc  : 读取Data
@Date  : 2020/10/16 21:22
'''
from Logger.GlobalLog import Logger
logger = Logger.write_log()
request_data = []

def loadRequestData(filePath):
    logger.info("开始读取数据")
    file = open(filePath, 'r', encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        line = line.replace("RequestBody:", "").replace("openkey:", "").strip('\n').split(" ")
        request_data.append(line)
    return len(lines)
