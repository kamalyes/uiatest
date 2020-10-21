# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： ProxyPool.py
# Author : v_yanqyu
# Desc: 代理IP
# Date： 2020/10/12 18:25
'''

from Logger.GlobalLog import Logger
logger = Logger.write_log()
from Utils.RequestTools import HttpsServer

class GetProxy():
    @classmethod
    def get_page(self):
        """
        设置爬取的page的url
        :param conect 公共url部分
        :return:page
        """
        page = []
        conect = "https://www.kuaidaili.com/free/inha/"
        for i in range(1, 100):
            url = conect + str(i)
            page.append(url)
        return page

    @classmethod
    def get_content(self,page,headers,proxies):
        for i in range(0,len(page)):
            s = HttpsServer.get_main(page[i], headers=headers, proxies=proxies, timeout=1)
    def clean_data(self,data):
        logger.info("bb")

if __name__ == '__main__':
    proxies = HttpsServer.proxy_state()
    proxy_page = GetProxy.get_page()
    headers = HttpsServer.get_header()
