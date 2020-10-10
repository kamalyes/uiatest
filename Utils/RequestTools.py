# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： RequestTools.py
# Author :  v_yanqyu
# Desc:    网络请求封装
# Date： 2020/10/9 11:19
'''
import json,requests
import configparser
from Logger import GlobalLog
logger = GlobalLog.Logger().write_log()#调用日志模块
from Utils import IniHandle
filepath = r'../Config/config.ini'
IniHandle = IniHandle.IniHandle()

class Https_Request():
    def proxy_state(self):
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
            if key == "proxy_switch" and value == "True":
                proxies = eval(dict.get(proxy_info, "proxy_type")) #强转为dict类型 否则 request模块识别不了str类型
                return proxies
            else:
                return value

    def get_main(self, url, params=None, headers=None, files=None, proxies=None, timeout=None):
        """
        封装get方法，return响应码和响应内容
        :param url: 请求的url地址
        :param params： 默认是以json格式化的一些参数
        :param headers: 头部信息（重要部分：Connection，Accept，Referer，Cookie，User-Agent）
        :param files:   文件 （默认get请求下很少使用这个）
        :param proxies: 代理 避免一些爬虫打击
        :param timeout: 等待超时间隔
        :return: status_code 状态码 response_json json_view下所有的内容
        """
        try:
            r = requests.get(url, params=params, headers=headers, files=files, proxies=proxies, timeout=5)
            logger.info("请求的内容：%s" % url)
            status_code = r.status_code  # 获取返回的状态码
            logger.info("获取返回的状态码:%d" % status_code)
            response_json = r.json()  # 响应内容，json类型转化成python数据类型
            logger.info("响应内容：%s" % response_json)
            cookies = requests.utils.dict_from_cookiejar(r.cookies)
            return status_code, response_json  # 返回响应码，响应内容
        except BaseException as e:
            logger.error("请求失败！", exc_info=1)

    def get_post(self, url, data=None, headers=None, files=None, proxies=None, timeout=None):
        """
        封装post请求，data形式传入，return响应码和响应内容
        :param url: 请求的url地址
        :param params： 默认是以json格式化的一些参数
        :param headers: 头部信息（重要部分：Connection，Accept，Referer，Cookie，User-Agent）
        :param files:   文件 （默认get请求下很少使用这个）
        :param proxies: 代理 避免一些爬虫打击
        :param timeout: 等待超时间隔
        :return: status_code 状态码 response_json json_view下所有的内容
        """
        try:
            r = requests.post(url, data=data, headers=headers, files=files, proxies=proxies, timeout=3)
            logger.info("请求的内容：%s" % data)
            status_code = r.status_code  # 获取返回的状态码
            logger.info("获取返回的状态码:%d" % status_code)
            response_json = r.json()  # 响应内容，json类型转化成python数据类型
            logger.info("响应内容：%s" % response_json)
            return status_code, response_json  # 返回响应码，响应内容
        except BaseException as e:
            logger.error("请求失败！", exc_info=1)

    def get_post_json(self, url, data=None, headers=None, proxies=None, timeout=None):
        """
        封装post方法，并用json格式传值，return响应码和响应内容
        :param url: 请求的url地址
        :param params： 默认是以json格式化的一些参数
        :param headers: 头部信息（重要部分：Connection，Accept，Referer，Cookie，User-Agent）
        :param files:   文件 （默认get请求下很少使用这个）
        :param proxies: 代理 避免一些爬虫打击
        :param timeout: 等待超时间隔
        :return: status_code 状态码 response json_view下所有的内容
        """
        try:
            data = json.dumps(data).encode('utf-8')  # python数据类型转化为json数据类型
            r = requests.post(url, data=data, headers=headers, proxies=proxies, timeout=3)
            logger.info("请求的内容：%s" % data)
            status_code = r.status_code  # 获取返回的状态码
            logger.info("获取返回的状态码:%d" % status_code)
            response = r.json()  # 响应内容，json类型转化成python数据类型
            logger.info("响应内容：%s" % response)
            return status_code, response  # 返回响应码，响应内容
        except BaseException as e:
            logger.error("请求失败！", exc_info=1)


if __name__ == '__main__':
    proxies = Https_Request().proxy_state()
    print(proxies)
    # 测试get请求
    url = 'https://ias.qvideo.qq.com/cgi-bin/videohub/pop/haomabao_check_svr?bkn=1193504743&_=0.5556534626821834'
    headers = {"host": "ias.qvideo.qq.com",
               "sec-fetch-mode": "cors",
               "origin": "https://qvideo.qq.com",
               "user-agent": "Mozilla/5.0 (Linux; Android 9; SPN-AL00 Build/HUAWEISPN-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045332 Mobile Safari/537.36 V1_AND_SQ_8.4.10_0_RDM_B QQ/8.4.10.16019 NetType/WIFI WebP/0.3.0 Pixel/1080 StatusBarHeight/109 SimpleUISwitch/0 QQTheme/2101 InMagicWin/0",
               "referer": "https://qvideo.qq.com/qq/hongniang/index.html?asyncMode=3&from_id=20011&_wv=2&",
               "cookie": "uin=o0501893067; skey=Maq1JM3Rnh",
               "q-guid": "55a66c45d18693a78a925ef513b788cb",
               "q-qimei": "b4377178a349ff92",
               "connection": "close",
               "Content-Type": "application/json"}
    i = 1;
    while i <= 1:
        s = Https_Request().get_main(url, headers=headers, proxies=proxies, timeout=1)
        i += 1;
    print("已完成", i, "次")

    # payloda = {'city': '上海'}
    # Https_Request().get_main(url,  proxies=proxies,timeout=2)
    # #测试dict过滤