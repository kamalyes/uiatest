#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
# FileName： GlobalLog.py
# Author : v_yanqyu
# Desc: PyCharm
# Date： 2020/7/15 16:15
'''
__author__ = 'v_yanqyu'
import logging,shutil
import time,datetime
import os,configparser
conf_ini = r"../Config/config.ini"
conf = configparser.ConfigParser()
conf.read(conf_ini,encoding="utf-8")
log_dir = conf.get("Logger-Path", "log_dir")
def_dir = conf.get("Logger-Path", "def_log_dir")
err_dir = conf.get("Logger-Path", "error_log_dir")

class Logger(object):
    def write_log(self):
        """
        日志处理(写入文本、控制台输出)
        :param logs_path： 日志存储总路径
        :param all_log_path：info、default日志存放路径
        :param error_log_path：error日志存储路径
        :param date_file_path 区分日期创建文件夹
        :param all_log_name：默认日志文件名
        :param error_log_name：错误日志文件名
        :param console：控制台输出
        :return logger
        """
        # 获取项目的根目录
        project_path = os.getcwd()
        logs_path = os.path.join(project_path, log_dir)
        local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 日期文件夹路径
        date_file_path = os.path.join(logs_path, local_date)
        # 如果没有日期文件夹，创建该文件夹
        if not os.path.exists(date_file_path):
            os.makedirs(date_file_path)
        # 完整日志存放路径
        all_log_path = os.path.join(date_file_path, def_dir)
        # 如果没有完整日志文件夹，创建该文件夹
        if not os.path.exists(all_log_path) :
            os.makedirs(all_log_path)
        # 错误日志存放路径
        error_log_path = os.path.join(date_file_path, err_dir)
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

        # 提示：这里需要进行判断如果logger.handlers列表为空，则添加，否则直接去写日志 处理重复打印事件
        if not logger.handlers:
            logger.addHandler(defaul_log)
            logger.addHandler(error_log)
            logger.addHandler(console)
        return logger

    def delete_log(self,days=''):
        """
        大于多少天的日志自动删除
        :param today   获取当前时间
        :param offset  计算偏移量,前xxx天
        :param re_date 获取想要的日期的时间
        :param re_date_unix    前xxx天时间转换为时间戳
        :param isremove      扫描到的符合条件的文件新增至list
        :param not_conformity  不满足条件的文件list
        :param log_dir     config拉过来的文件目录
        :return:
        """
        today = datetime.datetime.now()
        offset = datetime.timedelta(days=days)
        re_date = (today + offset)
        re_date_unix = int(time.mktime(re_date.timetuple()))
        isremove = []
        not_conformity = []
        for dirpath, dirnames, filenames in os.walk(log_dir):
            timeArray = os.stat(dirpath).st_mtime
            if timeArray < re_date_unix:
                isremove.append(dirpath)
            else:
                not_conformity.append(dirpath)
        for i in range(len(isremove)):
            if i ==  0:
                continue
            else:
                head, tail = os.path.split(isremove[i])
                if tail in("Default_Logs","Error_Logs"):
                    continue
                else:
                    shutil.rmtree(isremove[i], ignore_errors=True)
        if os.path.exists(isremove[i]):
            logger.info("删除(%s)失败！！！"%(isremove[i]))
        else:
            logger.info("成功删除%s"%(isremove[i]))
        logger.info("过期的文件：%s" % (isremove))
        logger.info("不满足条件的文件：%s"%(not_conformity))

if __name__ == '__main__':
    logger = Logger().write_log()
    delete = Logger().delete_log(days=5)
    # 日志
    logger.debug('this is a logger debug message')
    logger.info('this is a logger info message')
    logger.warning('this is a logger warning message')
    logger.error('this is a logger error message')
    logger.critical('this is a logger critical message')