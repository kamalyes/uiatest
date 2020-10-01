# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  :MyLogger.py
@Author: v_yanqyu
@Desc  : MyLogger简易封装
@Date  :2020/9/26-10:22
'''

import time,logging
import os,configparser
conf_ini = r"../Config/config.ini"
conf = configparser.ConfigParser()
conf.read(conf_ini,encoding="utf-8")
log_dir = conf.get("Logger-Path", "log_dir")
def_dir = conf.get("Logger-Path", "def_log_dir")
err_dir = conf.get("Logger-Path", "error_log_dir")


LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

logger = logging.getLogger()
level = 'default'


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
    project_path = os.getcwd()
    logs_path = os.path.join(project_path, log_dir)
    local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    date_file_path = os.path.join(logs_path, local_date)
    if not os.path.exists(date_file_path):
        os.makedirs(date_file_path)
    all_log_path = os.path.join(date_file_path, def_dir)
    if not os.path.exists(all_log_path):
        os.makedirs(all_log_path)
    error_log_path = os.path.join(date_file_path, err_dir)
    if not os.path.exists(error_log_path):
        os.makedirs(error_log_path)
    local_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # 设置日志文件名
    all_log_name = all_log_path + local_time + '.log'
    error_log_name = error_log_path + local_time + '.log'
    date = '%Y-%m-%d %H:%M:%S'
    # 将日志输出到屏幕
    console = logging.StreamHandler()
    console.setLevel(LEVELS.get(level, logging.NOTSET))
    # 将日志输出到文件
    logger.setLevel(LEVELS.get(level, logging.NOTSET))
    handler = logging.FileHandler(all_log_name, encoding='utf-8')
    err_handler = logging.FileHandler(error_log_name, encoding='utf-8')

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
