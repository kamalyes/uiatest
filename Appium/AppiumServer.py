# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# Author : YuYanQing
# Desc: 初始化APPIUM服务
# Date： 2020/11/6 19:07
'''

import os
import re
import socket
from time import sleep
from appium import webdriver
from Logger.GlobalLog import Logger
from Utils.DirTools import DocProcess
logger = Logger.write_log()

class InitAppiumConf():

    @classmethod
    def killServer(self):
        """
        清理appium环境,杀node.exe的进程
        :return:
        """
        server_list = os.popen('tasklist | find "node.exe"').readlines()
        if len(server_list)>0:
            logger.info("捕捉到Node进程：%s"%(server_list))
            os.popen("taskkill -F -PID node.exe")
        elif len(server_list)<=0:
            logger.info("暂时没有启动过Node相关服务")

    @classmethod
    def startServer(self,ip, port,device):
        """
        启动Appium服务
        :param ip:
        :param port:
        :return:
        """
        if self.checkPort(ip, str(port)) == True:
            text = "@echo off\ntitle start Appium Server {}\ncmd /c \"appium -a {} -p {} -bp {} -U {} --no-reset --session-override\"".format(
                ip, ip, str(port),port+1,device)
            file = open('../Config/start_appium.bat', 'w')  # 以覆盖的形式写入
            file.write(text)
            file.close()
            logger.info("正在启动Appium服务{IP：%s,Port：%s}" % (ip, str(port)))
            batPath = DocProcess.getSuperiorDir()+r"\Config\start_appium.bat"
            os.system(batPath)
        else:
            logger.error("端口-%s被占用，请手动重启！" % (str(port)))

    @classmethod
    def getDeviceIds(self):
        """
        获取连接设备的设备ID
        :param deviceIds 存储ID容器
        :return:
        """
        Ids_info = list(os.popen("adb devices").readlines())
        deviceIds = []
        # 使用正则获取连接设备的设备ID 20201106  GWY0216C15005982
        for i in range(1, len(Ids_info) - 1):
            id = re.findall(r"^\w*\b", Ids_info[i])[0]
            deviceIds.append(id)
        return deviceIds

    @classmethod
    def depolyDev(self,platform_name,app_package,app_activity):
        # 获取设备ID
        devicesIds = self.getDeviceIds()
        if not (platform_name  and app_package and app_activity):
            logger.error("应用程序选择初始失败！")
        else:
            for dev in devicesIds:
                desired_caps = {
                    "platformName": platform_name,
                    "deviceName": dev,
                    "appPackage": app_package,
                    "appActivity": app_activity
                }
                logger.info(desired_caps)

    @classmethod
    def checkPort(slef,host,port):
        """
        检查端口是否被占用
        :param host: ip地址
        :param port: 端口号
        :return:
        """
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            sock.connect((str(host),int(port)))
            sock.shutdown(2)  #表示将来禁止读和写
        except OSError as msg:
            # logger.info("端口：%s 未启用" %(port))
            # logger.info(msg)
            return True
        else:
            return False

    @classmethod
    def releasePort(self,port):
        """
        释放指定端口
        :param port:
        :return:
        """
        cmd_find = 'netstat -ano | findstr %s' %port
        result = os.popen(cmd_find).read()
        if str(port) and 'LISTENING' in result:
            #获取端口对应的pid进程
            i = result.index('LISTENING')
            # 'LISTENING'与端口号之间相隔7个空格
            start = i + len('LISTENING') +7
            end = result.index('\n')
            pid = result[start:end]
            #关闭被占用端口的pid
            cmd_kill = 'taskkill -f -pid %s' %pid
            logger.info("正在关闭端口：%s"%(cmd_kill))
            os.popen(cmd_kill)
        else:
            logger.error('端口：%s 未启用' %port)

if __name__ == '__main__':
    # InitAppiumConf.depolyDev('Android',  'com.tencent.now', 'com.tencent.now.app.startup.LauncherActivity')
    # print(InitAppiumConf.checkPort("127.0.0.1", "5926"))
    # InitAppiumConf.releasePort(555)
    # InitAppiumConf.startServer("127.0.0.1", 5920)

    # 杀掉所有Node相关服务具体看业务是否需要每次运行都操作
    # InitAppiumConf.killServer()
    InitAppiumConf.startServer("127.0.0.1", 5920,"D8H6R19630008844")
    # InitAppiumConf.startServer("127.0.0.1", 5920)

