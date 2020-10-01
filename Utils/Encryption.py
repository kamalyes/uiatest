# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : Encryption.py
@Author: v_yanqyu
@Desc  : 加密算法
@Date  : 2020/9/25 19:35
'''
import base64
import binascii
from hashlib import sha1,md5
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Logger import GlobalLog

logger = GlobalLog.Logger().write_log() #导入日志模块

str1 = "你好"

class Decode():
    def base64_encrypt(self):
        """
        binary 需要转成2进制格式才可以转换，所以我们这里再手动转换一下
        :return:
        """
        binary = base64.b64encode(str1.encode())
        logger.info(binary)
        return binary

    def md5_encrypt(self,decode_msg):
        """
        md5 算法加密
        :param decode_msg: 需加密的字符串
        :return: 加密后的字符
        """
        hl = md5()
        hl.update(decode_msg.encode('utf-8'))
        return hl.hexdigest()


    def sha1_encrypt(self,decode_msg):
        """
        sha1 算法加密
        :param decode_msg: 需加密的字符串
        :return: 加密后的字符
        """
        sh = sha1()
        sh.update(decode_msg.encode('utf-8'))
        return sh.hexdigest()

    
    def sha256_encrypt(self,decode_msg):
        """
        sha256 算法加密
        :param decode_msg: 需加密的字符串
        :return: 加密后的字符
        """
        sh = SHA256.new()
        sh.update(decode_msg.encode('utf-8'))
        return sh.hexdigest()

    def des_encrypt(self,decode_msg, key):
        """
        DES 算法加密
        :param decode_msg: 需加密的字符串,长度必须为8的倍数，不足添加'='
        :param key: 8个字符
        :return: 加密后的字符
        """
        de = DES.new(key, DES.MODE_ECB)
        mss = decode_msg + (8 - (len(decode_msg) % 8)) * '='
        text = de.encrypt(mss.encode())
        return binascii.b2a_hex(text).decode()


    def aes_encrypt(self,decode_msg, key, vi):
        """
        AES 算法的加密
        :param decode_msg: 需加密的字符串
        :param key: 必须为16，24，32位
        :param vi: 必须为16位
        :return: 加密后的字符
        """
        obj = AES.new(key, AES.MODE_CBC, vi)
        txt = obj.encrypt(decode_msg.encode())
        return binascii.b2a_hex(txt).decode()



if __name__ == '__main__':
    Decode().base64_encrypt()
    Decode().base64_decrypt(binary= Decode().base64_encrypt())
    print(Decode().md5_encrypt('你好'))

