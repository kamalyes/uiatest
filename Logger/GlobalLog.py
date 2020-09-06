#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
# FileName： GlobalLog.py
# Author : v_yanqyu
# Desc: PyCharm
# Date： 2020/7/15 16:15
'''
__author__ = 'v_yanqyu'
import logging
import time,datetime
import os
class Logger(object):
    def write_log():
        # 获取项目的根目录
        project_path = os.getcwd()
        Logs_path = os.path.join(project_path, '../Result/Logs')
        # 获取本地时间，转为年-月-日格式
        # 获取当前时间
        today = datetime.datetime.now()
        local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 日期文件夹路径
        date_file_path = os.path.join(Logs_path, local_date)
        # 如果没有日期文件夹，创建该文件夹
        if not os.path.exists(date_file_path):
            os.makedirs(date_file_path)
        # 完整日志存放路径
        all_log_path = os.path.join(date_file_path, 'Default_Logs/')
        # 如果没有完整日志文件夹，创建该文件夹
        if not os.path.exists(all_log_path):
            os.makedirs(all_log_path)
        # 错误日志存放路径
        error_log_path = os.path.join(date_file_path, 'Error_Logs/')
        # 如果没有错误日志文件夹，创建该文件夹
        if not os.path.exists(error_log_path):
            os.makedirs(error_log_path)
        # 获取本地时间，转为年月日时分秒格式
        local_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 设置日志文件名
        all_log_name = all_log_path + local_time + '.log'
        error_log_name = error_log_path + local_time + '.log'

        # 创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # 创建defaul_log_handler写入所有日志
        defaul_log = logging.FileHandler(all_log_name,encoding='utf-8')
        defaul_log.setLevel(logging.DEBUG)

        # 创建error_log_handler写入所有日志
        error_log = logging.FileHandler(error_log_name,encoding='utf-8')
        error_log.setLevel(logging.ERROR)

        # 创建console_handler写入所有日志
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        # 定义default日志输出格式 以时间-日志器名称-日志级别-日志内容的形式展示
        all_log_formatter = logging.Formatter("%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s: %(message)s")

        # 定义error日志输出格式  以时间-日志器名称-日志级别-文件名-函数行号-错误内容
        error_log_formatter = logging.Formatter("%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s: %(message)s")

        # 将定义好的输出形式添加到handler
        defaul_log.setFormatter(all_log_formatter)
        console.setFormatter(all_log_formatter)
        error_log.setFormatter(error_log_formatter)

        # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
        if not logger.handlers:
            logger.addHandler(defaul_log)
            logger.addHandler(error_log)
            logger.addHandler(console)
        # 添加下面一句，在记录日志之后移除句柄
        return logger

    def delete_log(days=''):
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
            # print("当前日期", today.strftime('%Y-%m-%d'))  # 当前日期
            # print("前{}天日期".format(days).replace("-",""), re_date.strftime('%Y-%m-%d'))  # 前自定义多少天日期
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
    logger = Logger.write_log()
    delete = Logger.delete_log(days=-5)
    # 日志
    logger.debug('this is a logger debug message')
    logger.info('this is a logger info message')
    logger.warning('this is a logger warning message')
    logger.error('this is a logger error message')
    logger.critical('this is a logger critical message')