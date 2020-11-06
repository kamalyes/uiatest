# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： GeneralTools.py
# Author :  v_yanqyu
# Desc:    网络请求封装
# Date： 2020/10/9 11:19
'''
import json
import os
import random
import requests as requests
from faker import Factory
from Logger.GlobalLog import Logger  # 导入日志模块
from Utils.ConfigParser import IniHandle
from Utils.DictClean import YamlHandle
logger = Logger.write_log()   # 调用日志模块
IniHandle =  IniHandle()
requests.packages.urllib3.disable_warnings()

class HttpsServer():
    def __init__(self):
        self.seesion = requests.Session
        print(requests.Session)

    @classmethod
    def proxyState(self):
        """
        解析ini配置文件 拉取proxy_switch状态返回所需结果
        :param sections 读取的ini节点路径
        :return: proxies：正常开启状态下返回代理配置键值对类似于 {'http': 'http://localhost:12639', 'https': 'http://localhost:12639'}
        开关状态关闭的情况下才会返回value即：False
        """
        try:
            off_status = IniHandle.optvalue(node='Proxy_Setting',key='proxy_switch')
            if off_status is not  None:
                proxies = IniHandle.optvalue(node='Proxy_Setting',key='proxy_type')
                logger.info(proxies)
                return proxies
        except Exception as ModuleNotFoundError:
            logger.error(ModuleNotFoundError)

    @classmethod
    def randmoHeader(self,method=None):
        """
        生成不同的 user-agent
        :param method 方式 默认自定义生成 若无填写则工厂生成
        :return: user_agent
        """
        user_agent = [
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60'
                    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
                    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
                    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
                    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
                    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
                    'Mozilla/5.0 (Linux; Android 9; SPN-AL00 Build/HUAWEISPN-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 HuaweiBrowser/9.1.1.307 Mobile Safari/537.36',
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'

                ]
        if method == "factoty":
            user_agent.clear()
            factory = Factory.create()
            user_agent.append({'User-Agent': factory.user_agent()})
            logger.info("FactoryUserAgent方法产生：%s"%(user_agent[0]))
            return user_agent[0]
        else:
            user_agent = random.choice(user_agent)
            logger.info("自定义随机产生：%s"%(user_agent))
            return user_agent

    @classmethod
    def getResponse(self,response):
        """
        将获取到的response数据存储至yaml格式文本、后期也可以调用
        :param address 请求地址
        :param method 请求方式
        :param header 请求头部
        :param content 返回内容
        :param status_code 响应状态码
        :return:data
        """
        try:
            address = response.url
            method = response.request
            content = response.text
            headers = response.headers
            status_code = response.status_code
            filepath = r'..\YamlData\Response%s.yaml'%('Json')
            data = {'address': address, 'method': str(method), 'content': str(content).encode('utf-8'), 'headers': str(headers),
                    'status_code': status_code}
            YamlHandle.writeyaml(filepath=filepath, data=data, method="a")
            data = YamlHandle.yamldata(filepath=filepath)
            return data
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)

if __name__ == '__main__':
    proxies = HttpsServer.proxyState()
    HttpsServer.randmoHeader()
    HttpsServer.randmoHeader(method="factoty")