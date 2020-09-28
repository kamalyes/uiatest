#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
@File  :Encryption.py
@Author:v_yanqyu
@Desc  : 加密算法
@Date  :2020/9/25-19:35
'''
import base64
from Logger import GlobalLog
logger = GlobalLog.Logger().write_log() #导入日志模块

str1 = "你好"

class Decode():
    def base64_crypto(self):
        """
        binary 需要转成2进制格式才可以转换，所以我们这里再手动转换一下
        :return:
        """
        binary = base64.b64encode(str1.encode())
        logger.info(binary)
        return binary

    def base64_decip(self,binary):
        temp = base64.b64decode(binary)
        print('解密后的结果 --> ', temp.decode())

if __name__ == '__main__':
    Decode().base64_crypto()
    Decode().base64_decip(binary= Decode().base64_crypto())

