# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： RequestTools.py
# Author :  v_yanqyu
# Desc:    网络请求封装
# Date： 2020/10/9 11:19
'''
import json,random,requests
from faker import Factory
from Utils import IniHandle
from Utils.DictClean import YamlHandle
from Logger.GlobalLog import  Logger # 导入日志模块
logger = Logger.write_log()#调用日志模块
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

    def get_header(self,user_agent,cookies=None,referer=None,host=None,origin=None):
        """
        请求头部信息
        :param user_agent: 用户代理浏览器标识
        :param cookies:    登录态信息
        :param host:       域名
        :param origin:     转发跨域
        :return:
        """
        return {'User-Agent': user_agent,
                'Host': host,
                'Origin': origin,
                'Cookie': cookies,
                'Referer': referer,
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Content-Type': 'application/json'}

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
            cookies = requests.utils.parse_dict_header(r.cookies)
            return status_code, response_json,cookies  # 返回响应码，响应内容
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

    def get_post_json(self, url, method,json=None,headers=None, proxies=None, timeout=None):
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
            playload = YamlHandle.StrToJson(method,string=json)
            r = requests.post(url, params=playload, headers=headers, proxies=proxies, timeout=3)
            logger.info("请求的接口：%s" % url)
            status_code = r.status_code  # 获取返回的状态码
            logger.info("获取返回的状态码:%d" % status_code)
            response = r.json()  # 响应内容，json类型转化成python数据类型
            logger.info("响应内容：%s" % response)
            return status_code, response  # 返回响应码，响应内容
        except BaseException as e:
            logger.error("请求失败！", exc_info=1)

Https_Request = Https_Request()

if __name__ == '__main__':
    proxies = Https_Request.proxy_state()
    logger.info(proxies)
    user_agent = Https_Request.get_user_agent(num=5,method='custom')
    headers = Https_Request.get_header(user_agent,cookies="uin=o3537095926; skey=M37gJTZ8U4")
    # 测试get请求
    url = 'https://ias.qvideo.qq.com/cgi-bin/videohub/pop/haomabao_check_svr?bkn=1193504743&_=0.5556534626821834'
    # headers = {"host": "ias.qvideo.qq.com",
    #            "sec-fetch-mode": "cors",
    #            "origin": "https://qvideo.qq.com",
    #            "user-agent": "Mozilla/5.0 (Linux; Android 9; SPN-AL00 Build/HUAWEISPN-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045332 Mobile Safari/537.36 V1_AND_SQ_8.4.10_0_RDM_B QQ/8.4.10.16019 NetType/WIFI WebP/0.3.0 Pixel/1080 StatusBarHeight/109 SimpleUISwitch/0 QQTheme/2101 InMagicWin/0",
    #            "referer": "https://qvideo.qq.com/qq/hongniang/index.html?asyncMode=3&from_id=20011&_wv=2&",
    #            "cookie": "uin=o3537095926; skey=M37gJTZ8U4",
    #            "connection": "close",
    #            "Content-Type": "application/json"}
    i = 1;
    while i <= 1:
        s = Https_Request.get_main(url, headers=headers, proxies=proxies, timeout=1)
        s = Https_Request.get_post_json(url,json="staticpage=sQsjulfPwmSj1e%3D&traceid=F90C0001&callback=parentowxe&time=1602858806&alg=v3&sig=eFh4clp0cXh", headers=headers, proxies=proxies, timeout=1)

        i += 1;
    print("已完成", i, "次")

    # payloda = {'city': '上海'}
    # Https_Request().get_main(url,  proxies=proxies,timeout=2)
    # #测试dict过滤