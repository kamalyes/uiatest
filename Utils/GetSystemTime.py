#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
# FileName： GetSystemTime.py
# Author : v_yanqyu
# Desc: 时间获取类
# Date： 2020/9/17 19:05
'''
__author__ = 'v_yanqyu'
import os
import time
import datetime
from Logger import GlobalLog
logger = GlobalLog.Logger.write_log()

class TimeUtil:

    def __init__(self, curtime=None):
        self.curtime = curtime

    def get_timestemp(self):
        """
        获取当前时间戳
        :return: get_timestemp
        """
        return time.time()

    def get_date(self):
        """
        获取当地日期的年月日
        :return get_date
        """
        return time.strftime("%Y-%m-%d")

    def get_time(self):
        """
        获取当地日期的时分秒
        :return: get_time
        """
        return time.strftime("%H:%M:%S")

    def get_datetime(self):
        """
        当地日期的年月日时分秒
        :return: get_datetime
        """
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def get_chinesedate(self):
        """
        当前本地日期的年月日
        :return: get_chinesedate
        """
        strTime = time.strftime("%Y-%m-%d", time.localtime())
        return strTime

    def get_chinesetime(self):
        """
        当前本地日期的时分秒
        :return: get_chinesetime
        """
        strTime = time.strftime("%H-%M-%S", time.localtime())
        return strTime

    def get_chinesedatetime(self):
        """
        当前本地日期的年月日时分秒
        :return: get_chinesedatetime
        """
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return strTime

    def compute_date(self, day_interval):
        """
        日期偏移
        :param day_interval: 想要偏移的天数
        :return compute_date
        """
        today = datetime.date.today()
        if isinstance(day_interval, int) and day_interval >= 0:
            return today + datetime.timedelta(days=day_interval)
        elif isinstance(day_interval, int) and day_interval < 0:
            return today - datetime.timedelta(days=abs(day_interval))

    def timestamp_to_date(self, timestamp):
        """
        时间戳格式化为xxx年xx月xx日
        :return timestamp_to_date
        :param timestamp:
        :return:
        """
        if not isinstance(timestamp, (int, float)):
            return None
        time_tuple = time.localtime(timestamp)

        return str(time_tuple[0]) + "年" + str(time_tuple[1]) + "月" + str(time_tuple[2]) + "日"

    def timestamp_to_time(self, timestamp):
        """
        时间戳格式化为xxx时xx分xx秒
        :param timestamp:
        :return: timestamp_to_time
        """
        if not isinstance(timestamp, (int, float)):
            return None
        time_tuple = time.localtime(timestamp)
        return str(time_tuple[4]) + "时" + str(time_tuple[5]) + "分" + str(time_tuple[6]) + "秒"

    def timestamp_to_datetime(self, timestamp):
        """
        时间戳格式化为xxx年xx月xx日xx时xx分xx秒
        :param timestamp:
        :return timestamp_to_datetime
        """
        return self.timestamp_to_date(timestamp) + self.timestamp_to_time(timestamp)

    def get_everyday(self, start, end):
        """
        中间时差计算
        :param start: 开始日期
        :param end:   结束日期
        :return getEveryDay
        """
        date_list = []
        begin_date = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        logger.info('中间共计%s天' %str(len(date_list)))
        return date_list

    def get_singtime(self, singletime):
        """
        单个日期初始化时间戳年月日时分秒、转化为时间戳
        :param singletime:
        :return time_stamp
        """
        singletime = time.strptime(singletime, '%Y-%m-%d %H:%M:%S')
        time_stamp = int(time.mktime(singletime))
        return time_stamp

if __name__ == "__main__":
    t = TimeUtil()
    logger.info(t.get_timestemp())
    logger.info(t.get_date())
    logger.info(t.get_time())
    logger.info(t.get_datetime())
    logger.info(t.get_chinesedate())
    logger.info(t.get_chinesetime())
    logger.info(t.get_chinesedatetime())
    logger.info(t.compute_date(10))
    logger.info(t.compute_date(-6))
    logger.info(t.timestamp_to_date(1600341939))
    logger.info(t.timestamp_to_time(1600341939))
    logger.info(t.timestamp_to_datetime(1600341939))
    logger.info(t.get_everyday("2020-06-01", "2020-07-01"))
    logger.info(t.get_singtime("2020-06-01 18:50:00"))
