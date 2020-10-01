# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName：GlobalLoguru.py
# Author : v_yanqyu
# Desc: 日志操作模块,屏幕输出/文件输出 可选(默认屏幕和文件均输出)
# Date： 2020/5/7 10:05
'''
__author__ = 'v_yanqyu'
import os
import time,datetime
from loguru import logger
class GlobalLoguru:
    def write_log(self):
        # 错误日志
        logger.add(
            os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), "Result/Logs/{time:YYYY-MM-DD}/Error_Logs/{time:YYYY-MM-DD}.log"),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message} ",
            filter=lambda x: True if x["level"].name == "ERROR" else False,
            rotation="500MB", retention=7, level='ERROR', encoding='utf-8',enqueue=True
        )
        # 成功日志
        logger.add(
            os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), "Result/Logs/{time:YYYY-MM-DD}/Success_Logs/{time:YYYY-MM-DD}.log"),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            filter=lambda x: True if x["level"].name == "SUCCESS" else False,
            rotation="500MB", retention=7, level='SUCCESS', encoding='utf-8',enqueue=True
        )
        # Default日志
        logger.add(
            os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), "Result/Logs/{time:YYYY-MM-DD}/Default_Logs/{time:YYYY-MM-DD}.log"),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            rotation="500MB", retention=7, level='DEBUG', encoding='utf-8',enqueue=True
        )

        self.logger = logger
        return self.logger

    def delete_log(self,days=''):
        # 定义文件路径
        filepath = r"../Result/Logs/"
        # 获取当前时间
        today = datetime.datetime.now()
        # 计算偏移量,前xxx天
        offset = datetime.timedelta(days=days)
        # 获取想要的日期的时间
        re_date = (today + offset)
        # 前xxx天时间转换为时间戳
        re_date_unix = int(time.mktime(re_date.timetuple()))
        print("当前日期", today.strftime('%Y-%m-%d'))  # 当前日期
        print("前{}天日期".format(days).replace("-",""), re_date.strftime('%Y-%m-%d'))  # 前自定义多少天日期
        try:
            for File_Path in os.listdir(filepath): #遍历检索当前目录下的所有子目录名称
                GeneralFile=filepath+File_Path # 拼接完整目录
                for LogFileName in os.listdir(GeneralFile): #检索文件名
                    TouchFileName = GeneralFile+"/"+LogFileName
                    file_time = LogFileName.replace(".log","") #提取文件名格式化
                    timeArray = time.strptime(file_time, "%Y-%m-%d")
                    timeStamp = int(time.mktime(timeArray))
                    if timeStamp < re_date_unix:
                        print("已删除过期{}天日志".format(days).replace("-",""),TouchFileName)
                        os.remove(TouchFileName)
                    else:
                        print("{}存活时间未超过{}天,无需处理!".format(TouchFileName,days).replace("-",""))
        except Exception as TypeError:
            print(TypeError)

if __name__ == '__main__':
    GlobalLoguru().delete_log(days=-6)
    logger=GlobalLoguru().write_log()
    logger.error("这是一个Error问题")
    logger.debug("这是一个Debug问题")
    logger.info("这是一个Info问题")
