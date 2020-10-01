# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  :CheckEnviron.py
@Author:v_yanqyu
@Desc  : 开始测试本地环境是否就位
@Date  :2020/9/21 15:05
'''
from Utils import LibraryTools
from Utils import AdbTools

adbManage = AdbTools.Adb_Manage()
jarManage = LibraryTools.JarManage()

class Environment(object):
    @classmethod
    def run(self):
        """
        :param adbManage.check_filtered 检查本地环境是Win还是linux
        :param jarManage.check_import    检查本地导入模块是否下载
        :return:
        """
        adbManage.check_filtered()
        jarManage.check_import(filepath=r'../requirements.txt')

Environment.run()