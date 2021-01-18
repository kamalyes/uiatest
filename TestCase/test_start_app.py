# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： test_start_app.py
# Author : MrYu
# Desc: //TODO
# Date： 2020/12/10 11:54
'''
from Appium.AppiumTools import AppDevice
import unittest
class UCTestCase(unittest.TestCase):
    def testCreateFolder(self):
        driver = AppDevice('127.0.0.1', 5920, 'Android', 'D8H6R19630008844', 'com.tencent.mobileqq',
                      'com.tencent.mobileqq.activity.SplashActivity', "D8H6R19630008844",6000)
if __name__ == "__main__":
    unittest.main()
