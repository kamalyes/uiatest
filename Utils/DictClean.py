# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： DictClean.py
# Author : v_yanqyu
# Desc: Yaml格式文本内容
# Date： 2020/10/9 17:11
'''
import yaml,json
from Logger.GlobalLog import Logger
from Utils import DirTools

logger = Logger.write_log()#调用日志模块

# 初始化列表、及yaml文件的异常抛出
tmp_list = []
yaml.warnings({'YAMLLoadWarning': False})  # 禁用加载器warnings报警

class YamlHandle():

    @classmethod
    def changetype(self,filepath):
        """
        Json或Yaml格式化
        :param target: 目标文件路径
        :param local:  转化源文件路径
        """
        try:
            with open(filepath, encoding='utf-8') as file:
                data = yaml.safe_load(file)
                dumps = json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))
                return dumps
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)
        finally:
            file.close()

    @classmethod
    def yamldata(self,filepath):
        """
        定义对应的yaml路径输出dict类型的data、
        :param filepath: 目标文件路径
        :return: data
        """
        try:
            with open(filepath, encoding='utf-8') as file:
                data = yaml.safe_load(file)
                if not isinstance(data, dict):
                    return False
                else:
                    return data
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)
        finally:
            file.close()

    @classmethod
    def getdict(self,key,data):
        """
        输出dict类型的data--value值
        :param filepath: 目标文件路径
        :return: tmp_list
        """
        if not isinstance(data, dict) or not isinstance(tmp_list, list):  # 对传入数据进行格式校验
            return 'argv[1] not an dict or argv[-1] not an list '
        logger.info("拆分数据---%s" % (data))
        if key in data.keys():
            tmp_list.append(data[key])

        for value in data.values():
            if isinstance(value, dict):
                self.getdict(key=key, data=value)
            elif isinstance(value, (list, tuple)):
                for mony in value:
                    if isinstance(mony, dict):
                        self.getdict(key=key, data=mony)
                    elif isinstance(mony, (list, tuple)):
                        self.getdict(key, data=mony)
        return tmp_list

    @classmethod
    def writeyaml(self,filepath,data,method):
        """
        将dict类型数据写入yaml
        :param filepath: 目标文件路径
        :param data:     json实体即dict类型的数据
        :param method:   w：全新写入、a：追加数据
        :param allow_unicode 处理乱码 content: "{\"ret\" : 1001,\"msg\: "请求参数错误(openid)"} -->'content': '{"ret" : 1001,"msg" : "请求参数错误(openid)
        """
        try:
            if method == "w":
                with open(filepath, "w", encoding="utf-8") as file:
                    yaml.dump(data, file,allow_unicode=True)
            elif method == "a":
                with open(filepath, "a+", encoding="utf-8") as file:
                    yaml.dump(data, file,allow_unicode=True)
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)
        finally:
            file.close()

    @classmethod
    def StrToJson(self,method=None,string=None):
        """
        Str文本内容与JSON格式互转
        :param method: 流转方式判断
        :param string: 字符
        :return: result：返回结果集 False：为空时返回
        """
        result = {}
        urlParamsStr = ''
        if method == "BodyToJson":
            str = string.split('&')
            for i in range(0, len(str)):
                string = str[i].split('=')
                result[string[0]] = string[1];
            logger.info("数据转化成功：%s"%(result))
            return result
        elif method == "JsonToBody":
            logger.info("检索到该Json有%s个键值对、开始清洗拼接数据！！！"%(len(string)))
            for key in string.keys():
                urlParamsStr += ('%s=%s&' % (key, string[key]))
            logger.info("数据转化成功：%s"%(urlParamsStr[:-1]))
            return urlParamsStr[:-1]
        else:
            logger.error("该内容不支持转换、请检查是否为JSON或Body类型")
            return False

if __name__ == '__main__':
    data = YamlHandle.yamldata(filepath = r'..\YamlData\Register.yaml')
    # logger.info(YamlHandle.getdict(key="name", data=data))
    # logger.info(YamlHandle.changetype(filepath=r'..\YamlData\Register.yaml'))
    # YamlHandle.writeyaml(filepath = r'..\YamlData\Token.yaml',data={'a':'b'},method="w")
    changetype =  YamlHandle.StrToJson(method="BodyToJson",string="staticpage=sQsjulfPwmSj1e%3D&traceid=F90C0001&callback=parentowxe&time=1602858806&alg=v3&sig=eFh4clp0cXh")
    changetype =  YamlHandle.StrToJson(method="JsonToBody",string={'staticpage': 'sQsjulfPwmSj1e%3D', 'traceid': 'F90C0001', 'callback': 'parentowxe', 'time': '1602858806', 'alg': 'v3', 'sig': 'eFh4clp0cXh'})