# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： AssertTools.py
# Author : YuYanQing
# Desc: Assert断言封装
# Date： 2020/10/10 18:18
'''
class Assertions:
    @classmethod
    def assert_keyword(self, value, expected_value):
        """
        验证关键值与预期结果是否一致
        :param value:
        :param expected_code:
        :return:
        """
        try:
            print("预期类型：%s，状态码：%s，实际类型：%s，状态码：%s。"%(type(value),value,type( expected_value),expected_value))
            if value == expected_value:
                return True
            elif value != expected_value:
                return False
        except Exception as TypeError:
            return TypeError

    @classmethod
    def assert_time(self, time, expected_time):
        """
        验证response响应时间小于预期最大响应时间,单位：毫秒
        :param time:
        :param expected_time:
        :return:
        """
        try:
            print("预期响应时间：%s，实际类型：%s。"%(time,expected_time))
            if time < expected_time:
                return True
            else:
                return False
        except:
            raise

if __name__ == '__main__':
    print(Assertions.assert_keyword("200",100))
    print(Assertions.assert_time(600,555))