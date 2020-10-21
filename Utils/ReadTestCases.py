# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : ReadTestCases.py
@Author: v_yanqyu
@Desc  : 调用Utils.ExcelTool工具类二次封装Excel操作
@Date  : 2020/10/21 23:27
'''

import configparser
from Utils.ExcelTools import *
from Logger.GlobalLog import Logger
logger =Logger.write_log()
from Utils.ConfigParser import IniHandle
conf = IniHandle.readconfig()

class OverallSitua():
    @classmethod
    def excel_data(self):
        """
        将excel数据转化为Dict便于其它模块调用
        :return:
        """
        filepath = conf.get("TestCase_Info", "InterfaceCase_Path")
        wookbook = ExcelHandle.open_excel(filepath)
        data = ExcelHandle.once_read(wookbook)
        return data

    @classmethod
    def data_formact(self,data=None):
        """
        接收data数据清洗一遍
        :return:
        """
        # 初始化公共key值、可在config中进行修改
        id = conf.get("TestCase_Info", "id")
        cata = conf.get("TestCase_Info", "cata")
        name = conf.get("TestCase_Info", "name")
        method = conf.get("TestCase_Info", "method")
        url = conf.get("TestCase_Info", "url")
        headers = conf.get("TestCase_Info", "headers")
        data = conf.get("TestCase_Info", "data")
        code = conf.get("TestCase_Info", "code")
        status = conf.get("TestCase_Info", "status")

        data = self.excel_data()
        for i in range(len(data)):
            di = data[i]
            # logger.info(type(dict))
            logger.info("%s%s"%(di.keys(),di.values()))



if __name__ == '__main__':
    OverallSitua.data_formact()