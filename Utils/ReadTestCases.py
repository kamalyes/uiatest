# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : ReadTestCases.py
@Author: v_yanqyu
@Desc  : 调用Utils.ExcelTool工具类二次封装Excel操作
@Date  : 2020/10/21 23:27
'''

from Utils.ExcelTools import *
from Logger.GlobalLog import Logger
logger =Logger.write_log()
from Utils.ConfigParser import IniHandle
IniHandle = IniHandle()

class OverallSitua():
    @classmethod
    def excelData(self):
        """
        将excel数据转化为Dict便于其它模块调用
        :return:
        """
        filepath = IniHandle.optvalue(node='TestCase_Info', key='InterfaceCase_Path')
        wookbook = ExcelHandle.open_excel(filepath)
        data = ExcelHandle.once_read(wookbook)
        return data

    @classmethod
    def dataFormact(self,data=None):
        """
        接收data数据清洗一遍
        :return:
        """
        # 初始化公共key值、可在config中进行修改
        id = IniHandle.optvalue(node='TestCase_Info', key='id')
        cata = IniHandle.optvalue(node='TestCase_Info', key='cata')
        name = IniHandle.optvalue(node='TestCase_Info', key='name')
        method = IniHandle.optvalue(node='TestCase_Info', key='method')
        url = IniHandle.optvalue(node='TestCase_Info', key='url')
        headers = IniHandle.optvalue(node='TestCase_Info', key='headers')
        data = IniHandle.optvalue(node='TestCase_Info', key='data')
        code = IniHandle.optvalue(node='TestCase_Info', key='code')
        status = IniHandle.optvalue(node='TestCase_Info', key='status')

        data = self.excelData()
        for i in range(len(data)):
            di = data[i]
            # logger.info(type(dict))
            logger.info("%s%s"%(di.keys(),di.values()))

if __name__ == '__main__':
    OverallSitua.dataFormact()