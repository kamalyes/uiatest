#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
@File  :MyLogger.py
@Author: v_yanqyu
@Desc  : 简易封装
@Date  :2020/9/26-10:22
'''

import logging
import os
import time

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

logger = logging.getLogger()
level = 'default'


def create_file(filename):
    path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()
    else:
        pass

def set_handler(levels):
    if levels == 'error':
        logger.addHandler(MyLog.err_handler)
    logger.addHandler(MyLog.handler)
    logger.addHandler(MyLog.console)


def remove_handler(levels):
    if levels == 'error':
        logger.removeHandler(MyLog.err_handler)
    logger.removeHandler(MyLog.handler)
    logger.removeHandler(MyLog.console)


def get_current_time():
    return time.strftime(MyLog.date, time.localtime(time.time()))


class MyLog:
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
    if not os.path.exists(all_log_path):
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
    create_file(all_log_name)
    create_file(error_log_name)
    date = '%Y-%m-%d %H:%M:%S'
    # 将日志输出到屏幕
    console = logging.StreamHandler()
    console.setLevel(LEVELS.get(level, logging.NOTSET))
    # 将日志输出到文件
    logger.setLevel(LEVELS.get(level, logging.NOTSET))
    handler = logging.FileHandler(log_file, encoding='utf-8')
    err_handler = logging.FileHandler(err_file, encoding='utf-8')

    @staticmethod
    def debug(log_meg):
        set_handler('debug')
        logger.debug("[DEBUG " + get_current_time() + "]" + log_meg)
        remove_handler('debug')

    @staticmethod
    def info(log_meg):
        set_handler('info')
        logger.info("[INFO " + get_current_time() + "]" + log_meg)
        remove_handler('info')

    @staticmethod
    def warning(log_meg):
        set_handler('warning')
        logger.warning("[WARNING " + get_current_time() + "]" + log_meg)
        remove_handler('warning')

    @staticmethod
    def error(log_meg):
        set_handler('error')
        logger.error("[ERROR " + get_current_time() + "]" + log_meg)
        remove_handler('error')

    @staticmethod
    def critical(log_meg):
        set_handler('critical')
        logger.error("[CRITICAL " + get_current_time() + "]" + log_meg)
        remove_handler('critical')


if __name__ == "__main__":
    MyLog.debug("This is debug message")
    MyLog.info("This is info message")
    MyLog.warning("This is warning message")
    MyLog.error("This is error")
    MyLog.critical("This is critical message")
