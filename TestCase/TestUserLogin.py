# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： RunTest.py
# Author : YuYanQing
# Desc: 用户登录
# Date： 2020/7/15 16:15
'''
import unittest
from Utils.OkHttps import Prepare
Prepare = Prepare()
class TestClass(unittest.TestCase):
    """ 用户登录 （说明）"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_login(self):
        """ 正确账号&密码（子函数说明） """
        try:
            res = Prepare.send_requests("https://www.baidu.com", "post", "json")
            status_code = Prepare.get_status_code(res)
            self.assertEqual(status_code, 200, "请求成功")
        except AssertionError:
            raise

if __name__ == "__main__":
    unittest.main()
