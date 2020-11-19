# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： RequestTools.py
# Author :  v_yanqyu
# Desc:    网络请求封装
# Date： 2020/10/9 11:19
'''
import json
import os
import random
import requests as requests
from faker import Factory
from requests_toolbelt import MultipartEncoder
from Logger.GlobalLog import Logger  # 导入日志模块
from Utils.ConfigParser import IniHandle
from Utils.CheckStatus import CodeWriting
from Utils.DictClean import YamlHandle
logger = Logger.write_log()   # 调用日志模块
IniHandle =  IniHandle()

class HttpsServer():
    def __init__(self):
        self.seesion = requests.Session

    @classmethod
    def proxy_state(self):
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
                return proxies
        except Exception as ModuleNotFoundError:
            logger.error(ModuleNotFoundError)

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
    def send_request(self, url, method,agreement=None,filepath=None,cookies =None,content_type=None,data=None):
        """
        :param url: 请求地址
        :param data: 传参数据
        :param header: 头部信息
        :param filepath：文件位置 str类型绝对路径
        :param agreement 协议 Https 则加密的SLL Http则普通协议 不填则默认return url
        :return: response 返回基本信息
        """
        try:
            if agreement == 'https':
                address = 'https://%s' % (url)
            elif agreement == 'http':
                address = 'http://%s' % (url)
            else:
                address = url
            logger.info(address)

            headers = self.get_header()

            if cookies is not None:
                headers['Cookies'] = cookies
            else:
                logger.warning("未携带Cookies信息上来，请注意是否会存在有登录态失效问题！！！")

            if content_type in('from','From','FROM'):
                headers['Content-Type'] = "application/x-www-form-urlencoded"

            elif content_type in('text/html','Text/Html', 'TEXT/HTML'):
                headers['Content-Type'] = "text/html;charset=utf-8"

            elif content_type in ('json','Json','JSON'):
                headers['Content-Type'] = "application/json; charset=utf-8"

            else:
                headers['Content-Type'] = "application/json; charset=utf-8"
                logger.warning("%s不支持类型-->后面操作默认Json定义,若有问题则请在方法中添加content_type类型为表单/文本/Json类型" % (content_type))

            if method in ('get','Get','GET'):
                logger.info("get请求！！！")
                response = requests.get(address, params=data, headers=headers,verify=False)

            elif  method in ('post','Post','POST'):
                logger.info("正在对地址：%s 发起Post请求！！！" % (address))
                if type(data) == dict:
                    data = json.dumps(data).encode(encoding='utf-8')
                    response = requests.post(address, json=data, headers=headers, timeout=5)
                elif type(data) == str:
                    response = requests.post(address, data=data, headers=headers, timeout=5)
                else:
                    logger.error("请检查传入的data数据结构是否正确，暂只支持json、str类型的传参！！！")

            elif method in ('delete','Delete','DELETE'):
                logger.info("正在对地址：%s 发起Delete请求！！！" % (address))
                if type(data) == dict:
                    data = json.dumps(data).encode(encoding='utf-8')
                    response = requests.delete(address, json=data, headers=headers, timeout=5,verify=False)
                elif type(data) == str:
                    response = requests.delete(address, data=data, headers=headers, timeout=5,verify=False)
                else:
                    logger.warning("请检查传入的data数据结构是否正确，暂只支持json、str类型的传参！！！")

            elif method in ('put','Put','PUT'):
                logger.info("正在对地址：%s 发起Put请求！！！" % (address))
                if type(data) == dict:
                    data = json.dumps(data).encode(encoding='utf-8')
                    response = requests.put(address, json=data, headers=headers, timeout=5)
                elif type(data) == str:
                    response = requests.put(address, data=data, headers=headers, timeout=5)
                else:
                    logger.warning("请检查传入的data数据结构是否正确，暂只支持json、str类型的传参！！！")

            elif method in ('trace','Trace','TRACE'):
                logger.info("正在对地址：%s 发起Trace请求！！！" % (address))
                if type(data) == dict:
                    data = json.dumps(data).encode(encoding='utf-8')
                    response = requests.trace(address, json=data, headers=headers, timeout=5)
                elif type(data) == str:
                    response = requests.trace(address, data=data, headers=headers, timeout=5)
                else:
                    logger.warning("请检查传入的data数据结构是否正确，暂只支持json、str类型的传参！！！")

            elif method in ('head','Head','HEAD'):
                logger.info("正在对地址：%s 发起Head请求！！！" % (address))
                if type(data) == dict:
                    data = json.dumps(data).encode(encoding='utf-8')
                    response = requests.head(address, json=data, headers=headers, timeout=5)
                elif type(data) == str:
                    response = requests.head(address, data=data, headers=headers, timeout=5)
                else:
                    logger.warning("请检查传入的data数据结构是否正确，暂只支持json、str类型的传参！！！")

            elif method in ('options','Options','OPTIONS'):
                logger.info("正在对地址：%s 发起Options请求！！！" % (address))
                if type(data) == dict:
                    data = json.dumps(data).encode(encoding='utf-8')
                    response = requests.options(address, json=data, headers=headers, timeout=5)
                elif type(data) == str:
                    response = requests.options(address, data=data, headers=headers, timeout=5)
                else:
                    logger.warning("请检查传入的data数据结构是否正确，暂只支持json、str类型的传参！！！")

            elif method in ('patch','Patch','PATCH'):
                logger.error("patch这种方式使用比较少暂时不做详细的修饰,需要使用则需去掉注释再次调试下！！！")
                # logger.info("正在对地址：%s 发起Patch请求！！！" % (address))
                # if type(data) == dict:
                #     data = json.dumps(data).encode(encoding='utf-8')
                #     response = requests.patch(address, json=data, headers=headers, timeout=5)
                # elif type(data) == str:
                #     response = requests.patch(address, data=data, headers=headers, timeout=5)
                # else:
                # logger.warning("请检查传入的data数据结构是否正确，暂只支持json、str类型的传参！！！")

            elif method in ('upload','Upload','UPLOAD'):
                # print(type(data))
                logger.info("正在对地址：%s 发起上传文件请求" % (address))
                # 利用os的切片得到tail即文件名
                head, tail = os.path.split(filepath)
                logger.info("传参时所需的文件名：%s" % (tail))
                logger.info(headers)
                files = {'file': open(filepath, 'rb').read()}  # 流式上传
                # 将请求的参数转换成 MultipartEncoder格式
                encode_data = MultipartEncoder(files)
                content_type = {'Content-Type': encode_data.content_type}
                headers.update(content_type)
                logger.info("请求头部信息：%s" % (headers))
                response = requests.post(url=url, headers=headers, data=data, files=files, timeout=5)

            else:
                logger.warning("暂不支持%s类型请求！！！" % (method))

            # 请求头部信息注入yaml
            YamlHandle.writeyaml(filepath=r'..\YamlData\Headers.yaml', data=headers, method="w")

            if response.status_code == 200:
                response = HttpsServer.get_response(response=response)
                logger.info("响应实体：%s" % (response))
                # 写入响应yaml
                YamlHandle.writeyaml(filepath=r'..\YamlData\ResponseJson.yaml', data=response, method="w")
                return response
            else:
                CodeWriting.notice("%s" % (response.status_code))
        except Exception as e:
            logger.error("异常抛出%s"%(e))

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
            data = {'address': address, 'method': str(method), 'content': str(content).encode('utf-8'), 'headers': str(headers),
                    'status_code': status_code}
            YamlHandle.writeyaml(filepath=filepath, data=data, method="a")
            data = YamlHandle.yamldata(filepath=filepath)
            return data
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)

if __name__ == '__main__':
    proxies = HttpsServer.proxy_state()
    url = "https://nowpic.gtimg.com/feeds_pic/ajNVdqHZLLCWsvtZtXqSLIeV5D3icBicKfYWT1iad8rD3hKa0ruwwBg8A/"
    data = {"data":"value"}
    cookies = "openkey=openkey&xg_mid=&openid=501893067&format=json&session_id=hy_gameid&amode=1&offer_id=1450006664&session_token=&extend=&sdkversion=1.6.9v&pfkey=pfKey&pf=huyu_m-2001-android-861080041549585&session_type=st_dummy"
    HttpsServer.send_request(url=url,method='upload',filepath=r"..\Resources\DejaVuSans.ttf")
