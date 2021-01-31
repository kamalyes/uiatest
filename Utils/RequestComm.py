# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： RequestComm.py
# Author : YuYanQing
# Desc: request二次封装
# Date： 2021/2/1 0:37
'''
import json,requests
from Logger.GlobalLog import Logger

logger = Logger.write_log()

class OpenServlet():
    def __init__(self,cookies=None,auth=None,proxies=None):
        """
        :param cookies: 字典或CookieJar，Request中的cookie
        :param auth:   证书
        :param proxies: 代理
        """
        self.cookies = cookies
        self.auth = auth
        self.proxies = proxies
        self.session = requests.session()

    def do_get(self,url,params=None,headers=None,files=None,verify=True,stream=True,timeout=10):
        """
        get方式请求
        :param url:  请求地址
        :param headers: 头部信息
        :param timeout: 超时
        :return:
        """
        response = self.session.get(url, params=params, headers=headers, files=files,verify=verify, stream=stream,timeout=timeout)
        return response

    def do_post(self,url,params=None,headers=None,data=None,json=None,verify=True,stream=True,timeout=10):
        """
        post方式请求
        :param url:  请求地址
        :param headers: 头部信息
        :param timeout: 超时
        :return:
        """
        if data !=None and json ==None:
            response = self.session.post(url, params=params, headers=headers, data=data, verify=verify, stream=stream,timeout=timeout)
        elif data ==None and json !=None:
            response = self.session.post(url, params=params, headers=headers, json=json, verify=verify, stream=stream,timeout=timeout)
        return response


if __name__ == '__main__':
    print(OpenServlet().do_get("https://www.baidu.com"))
    q = OpenServlet().do_post("https://www.baidu.com",json={"a":1})


