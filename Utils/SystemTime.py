# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： SystemTime.py
# Author : v_yanqyu
# Desc: 时间获取类
# Date： 2020/9/17 19:05
'''
import time
import datetime
from Logger.GlobalLog import Logger
logger = Logger.write_log()#调用日志模块

class TimeUtil:

    def __init__(self, curtime=None):
        self.curtime = curtime

    @classmethod
    def getTimestemp(self):
        """
        获取当前时间戳
        :return:
        """
        return time.time()

    @classmethod
    def getDate(self):
        """
        获取当地日期的年月日
        :return
        """
        return time.strftime("%Y-%m-%d")

    @classmethod
    def getTime(self):
        """
        获取当地日期的时分秒
        :return:
        """
        return time.strftime("%H:%M:%S")

    @classmethod
    def getDateTime(self):
        """
        当地日期的年月日时分秒
        :return:
        """
        return time.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def getChinaDate(self):
        """
        当前本地日期的年月日
        :return:
        """
        strTime = time.strftime("%Y-%m-%d", time.localtime())
        return strTime

    @classmethod
    def getChinaTime(self):
        """
        当前本地日期的时分秒
        :return:
        """
        strTime = time.strftime("%H-%M-%S", time.localtime())
        return strTime

    @classmethod
    def getChinaDateTime(self):
        """
        当前本地日期的年月日时分秒
        :return:
        """
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return strTime

    @classmethod
    def computeDate(self, day_interval):
        """
        日期偏移
        :param day_interval: 想要偏移的天数
        :return
        """
        today = datetime.date.today()
        if isinstance(day_interval, int) and day_interval >= 0:
            return today + datetime.timedelta(days=day_interval)
        elif isinstance(day_interval, int) and day_interval < 0:
            return today - datetime.timedelta(days=abs(day_interval))

    @classmethod
    def timestampTodate(self, timestamp):
        """
        时间戳格式化为xxx年xx月xx日
        :return timestamp_to_date
        :param
        :return:
        """
        if not isinstance(timestamp, (int, float)):
            return None
        time_tuple = time.localtime(timestamp)
        specific_data = str(time_tuple[0]) + "-" + str(time_tuple[1]) + "-" + str(time_tuple[2]) + " " \
                        + str(time_tuple[3]) + ":" + str(time_tuple[4]) + ":" + str(time_tuple[5])
        return specific_data

    @classmethod
    def getEveryDay(self, start, end):
        """
        中间时差计算
        :param start: 开始日期
        :param end:   结束日期
        :return
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

    @classmethod
    def getSingTime(self, singletime):
        """
        单个日期初始化时间戳年月日时分秒、转化为时间戳
        :param singletime:
        :return
        """
        singletime = time.strptime(singletime, '%Y-%m-%d %H:%M:%S')
        time_stamp = int(time.mktime(singletime))
        return time_stamp

if __name__ == "__main__":
    logger.info(TimeUtil.getTimestemp())
    logger.info(TimeUtil.getDate())
    logger.info(TimeUtil.getTime())
    logger.info(TimeUtil.getDateTime())
    logger.info(TimeUtil.getChinaDate())
    logger.info(TimeUtil.getChinaTime())
    logger.info(TimeUtil.getChinaDateTime())
    logger.info(TimeUtil.computeDate(10))
    logger.info(TimeUtil.computeDate(-6))
    logger.info(TimeUtil.timestampTodate(1603282677.5209892))
    logger.info(TimeUtil.getEveryDay("2020-06-05", "2020-07-01"))
    logger.info(TimeUtil.getSingTime("2020-06-01 18:50:00"))
