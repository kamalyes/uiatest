# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： DictClean.py
# Author : YuYanQing
# Desc: Yaml格式文本内容
# Date： 2020/10/9 17:11
'''
import re,yaml,json
from Logger.GlobalLog import Logger
logger = Logger.write_log()#调用日志模块

# 初始化列表、及yaml文件的异常抛出
tmp_list = []
yaml.warnings({'YAMLLoadWarning': False})  # 禁用加载器warnings报警

class YamlHandle():
    @classmethod
    def changeType(self,filepath):
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
    def yamlData(self,filepath):
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
    def getDict(self,key,data):
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
                self.getDict(key=key, data=value)
            elif isinstance(value, (list, tuple)):
                for mony in value:
                    if isinstance(mony, dict):
                        self.getDict(key=key, data=mony)
                    elif isinstance(mony, (list, tuple)):
                        self.getDict(key, data=mony)
        return tmp_list

    @classmethod
    def writeYamlFile(self,filepath,data,method):
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
    def dataConver(self,method=None,string=None,frist=None,second=None):
        """
        Str文本内容与JSON格式及俩个List类型互转
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
            return result
        elif method == "JsonToBody":
            logger.info("检索到该Json有%s个键值对、开始清洗拼接数据！！！"%(len(string)))
            for key in string.keys():
                urlParamsStr += ('%s=%s&' % (key, string[key]))
            return urlParamsStr[:-1]
        elif method == "ListToDict":
            if len(frist) > len(second) or len(frist) < len(second):
                logger.info("List长度不一致")
            else:
                for i in range(len(frist)):
                    result[frist[i]] = second[i]
                return result
        else:
            logger.error("该内容不支持转换、请检查是否为JSON或Body或List类型")
            return False

    @classmethod
    def filterKey(self, filepath, target,keyword=None):
        """
        清洗运行的窗口日志、过滤出有效的activity
        :param filepath 读取的文件路径
        :param target 目标存储路径
        :param keyword 过滤的关键字
        :return:
        """
        result =[]
        try:
            for line in open(filepath):
                isspace = line.strip()
                if len(isspace) != 0:
                    display = re.compile("%s.*?.y"%(keyword)).findall(isspace)
                    if  len(display):
                        result.append(display[0])
            distinct= set(result)
            # 写入文本
            for i in distinct:
                file = open('%s'%(target), 'a')
                file.write('\n' + str(i))
                file.close()
            return distinct
        except Exception as FileNotFoundError:
            logger.error(FileNotFoundError)

if __name__ == '__main__':
    data = YamlHandle.yamlData(filepath = r'..\yamlData\Register.yaml')
    YamlHandle.getDict(key="name", data=data)
    YamlHandle.changeType(filepath=r'..\yamlData\Register.yaml')
    YamlHandle.writeYamlFile(filepath = r'Token.yaml',data={'a':'b'},method="w")
    YamlHandle.dataConver(method="BodyToJson",string="staticpage=sQsjulfPwmSj1e%3D&traceid=F90C0001&callback=parentowxe&time=1602858806&alg=v3&sig=eFh4clp0cXh")
    YamlHandle.dataConver(method="JsonToBody",string={'staticpage': 'sQsjulfPwmSj1e%3D', 'traceid': 'F90C0001', 'callback': 'parentowxe', 'time': '1602858806', 'alg': 'v3', 'sig': 'eFh4clp0cXh'})
    name = ['连发行', '凤芬林', '濮刚亨', '竺丹澜', '计发亮']
    verify = ['iUMayr', '5vSpIa', 'Iq0tvj', 'XZYvVm', 'gAPIDr']
    logger.info(YamlHandle.dataConver(method="ListToDict",frist=name,second=verify))
    YamlHandle.filterKey(filepath=r'..\Config\WhiteActivity.txt',keyword='com.tencent.now',target='..\Result\ActivityTemp')
