#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
# FileName： TestMain.py
# Author : v_yanqyu
# Desc: PyCharm
# Date： 2020/9/15 19:06
'''
__author__ = 'v_yanqyu'
from Common.Appium  import AppDevice

from Logger import GlobalLog
logger = GlobalLog.Logger.write_log()

device = AppDevice("Android", "cdad83b0", "com.mryu.video", "com.mryu.splash.SplashActivity")
logger.info("app启动")