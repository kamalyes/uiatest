# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： RunTest.py
# Author : YuYanQing
# Desc: 运行(指定)目录下的所有测试用例，并生成HTML测试报告
# Date： 2020/7/15 16:15
'''

import unittest
from Utils import HTMLTestReportCN
class RunAllTests(object):
    def __init__(self,case_path,report_path):
        self.case_path = case_path
        self.title = "接口自动化测试报告"
        self.description = "备注信息"
        self.report_path = report_path

    def run(self):
        test_suite = unittest.TestLoader().discover(self.case_path)
        # 启动测试时创建文件夹并获取报告的名字
        report_dir = HTMLTestReportCN.ReportDirectory(self.report_path)
        report_dir.create_dir(title=self.title)
        report_path = HTMLTestReportCN.GlobalMsg.get_value("report_path")
        file = open(report_path, "wb")
        runner = HTMLTestReportCN.HTMLTestRunner(stream=file, title=self.title, description=self.description, tester="MrYu")
        runner.run(test_suite)
        file.close()

if __name__ == "__main__":
    RunAllTests("TestCase","Result/").run()
