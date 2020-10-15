# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : Main.py
@Author: v_yanqyu
@Desc  : 
@Date  : 2020/10/16 21:26
'''
import time
from Pressure import JsonLoads
from Logger.GlobalLog import Logger
from Pressure import SyncCore

logger = Logger.write_log()

def check_param(threadCount, requestUrl, methods, params):
    if threadCount <= 0:
        logger.error("请求数量不能小于 0 ")
        exit(0)
    if str(methods).lower() != 'get' and str(methods).lower() != 'post':
        logger.error("请求方法错误")
        exit(0)
    if JsonLoads.check_url(requestUrl) is False:
        logger.error("请求地址格式错误")
        exit(0)
    if JsonLoads.check_json(params) is False:
        logger.error("JSON格式错误")
        exit(0)


# python3 main.py 50 POST xx
if __name__ == '__main__':

    thread_count = 1000
    method = 'GET'
    param = '{}'
    request_url = 'https://fastest.now.qq.com/mobile/hongniang/waiting.html?room_id=1900000312&_bid=4430'
    # # 多少秒执行完成 0代表并发
    slowTime = 0
    # url = ''
    # # 循环执行次数
    roundCount = 1
    # # 是否从文件读取数据
    read = False
    startTime = time.time()

    logger.info("读取数据消耗时间{}毫秒".format((time.time() - startTime) * 1000))
    check_param(thread_count - 1, request_url, method, param)
    SyncCore.start(slowTime, roundCount, thread_count, request_url, method, param, read)
