# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： RequestTools.py
# Author :  v_yanqyu
# Desc:    网络请求封装
# Date： 2020/10/9 11:19
'''
import urllib,random
from faker import Factory
from Utils import IniHandle
from Utils.DictClean import YamlHandle
from Logger.GlobalLog import  Logger # 导入日志模块
logger = Logger.write_log()#调用日志模块
filepath = r'../Config/config.ini'
IniHandle = IniHandle.IniHandle()

class HttpsRequest():
    @classmethod
    def proxy_state(self,off_status):
        """
        解析ini配置文件 拉取proxy_switch状态返回所需结果
        :param sections 读取的ini节点路径
        :return: proxies：正常开启状态下返回代理配置键值对类似于 {'http': 'http://localhost:12639', 'https': 'http://localhost:12639'}
        开关状态关闭的情况下才会返回value即：False
        """
        sections = IniHandle.readSectionItems(filepath)
        proxy_info = IniHandle.prettySecToDic('Proxy_Setting')
        for key in proxy_info:
            value = dict.get(proxy_info, key)
            if key == "proxy_switch" and value == "True" and off_status == 1:
                proxies = eval(dict.get(proxy_info, "proxy_type")) #强转为dict类型 否则 request模块识别不了str类型
                return proxies
            else:
                return value

    @classmethod
    def get_user_agent(self,num,method=None):
        """
        生成不同的 user-agent
        :param method 方式 默认自定义生成 若无填写则工厂生成
        :param num: 生成个数
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
        if method == "custom":
            return random.choice(user_agent)
        else:
            user_agent.clear()
            factory = Factory.create()
            for i in range(num):
                user_agent.append({'User-Agent': factory.user_agent()})
            return random.choice(user_agent)

    @classmethod
    def get_header(self):
        """
        请求头部信息
        :param user_agent: 用户代理浏览器标识
        :return:
        """
        user_agent = self.get_user_agent(num=5, method='custom')
        return {'User-Agent': user_agent}

    @classmethod
    def get_response(self,response):
        """
        将获取到的response数据存储至yaml格式文本、后期也可以调用
        :return:data
        """
        try:
            address = response.url
            method = response.request
            content = response.text
            headers = response.headers
            status_code = response.status_code
            filepath = r'..\YamlData\Response%s.yaml'%('Json')
            data = {'address': address, 'method': str(method), 'content': content, 'headers': str(headers),
                    'status_code': status_code}
            YamlHandle.writeyaml(filepath=filepath, data=data, method="a")
            data = YamlHandle.yamldata(filepath=filepath)
            return data
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)

if __name__ == '__main__':
    proxies = HttpsRequest.proxy_state(off_status=1)
