# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : ProxyNetwork.py
@Author: v_yanqyu
@Desc  : 获取存活的代理IP动态
@Date  : 2020/10/16 17:09
'''

from Logger.GlobalLog import  Logger # 导入日志模块
logger = Logger.write_log()#调用日志模块

from Logger.GlobalLog import Logger
logger = Logger.write_log()
from Utils.GeneralTools import HttpsServer

class GetProxy():
    @classmethod
    def getContent(self):
        """
        循环遍历爬取各子页面数据
        :param  page  设置爬取的url
        :param conect 公共url部分
        :return:page
        """
        page = []
        conect = "http://www.kuaidaili.com/free/inha/"
        for i in range(1, 100):
            url = conect + str(i)
            page.append(url)
        for i in range(0,len(page)):
            HttpsServer.send_request(url=page[i],method='get')
    def clean_data(self,data):
        logger.info("bb")

GetProxy.getContent()