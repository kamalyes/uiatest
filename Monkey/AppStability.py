# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： AppStability.py
# Author : v_yanqyu
# Desc: Monkey脚本
# Date： 2020/10/25 10:57
'''
import re,os,time
import subprocess
from Logger.GlobalLog import Logger
from Utils.ConfigParser import  IniHandle
from Utils.DirTools import  DocProcess
from Utils.AdbTools import Adb_Manage
Adb = Adb_Manage()
logger = Logger.write_log()
getpwd =DocProcess.getSuperiorDir()
class Monkey():
    def __init__(self):
        """
        初始全局运行method/commod
        :param method 运行方式 默认存储sdcard 加特殊条件则存储至local
        :param commod  命令
        """
        # 文件读取及存储的路径
        self.AndroidFile =r"/sdcard/AutoMonkeyTest/"
        self.Today = time.strftime("%Y%m%d%H%M%S")
        self.remove = IniHandle.optValue(node="Monkey_Test",key="removeDir")
        if self.remove =="True":
            os.popen("adb shell ''rm -rf %s''" % (self.AndroidFile))
        os.popen("adb shell ''mkdir %s''" % (self.AndroidFile))
        self.killMonkey = IniHandle.optValue(node="Monkey_Test",key="killMonkey")
        self.package = IniHandle.optValue(node="Monkey_Test",key="package")
        self.grepMonkey = IniHandle.optValue(node="Monkey_Test",key="grepMonkey")
        self.whiteapath = IniHandle.optValue(node="Monkey_Test",key="whiteapath")
        self.apkpath =os.path.join(getpwd,IniHandle.optValue(node="Monkey_Test",key="apkpath"))
        self.local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # commod 命令
        self.operation = IniHandle.optValue(node="Monkey_Test",key="operation")
        self.ignore =  IniHandle.optValue(node="Monkey_Test",key="ignore")
        self.commod = ('%s %s'%(self.operation,self.ignore))
        # MAinActivity&白名单窗口
        self.mainactivity = IniHandle.optValue(node="Monkey_Test",key="mainactivity")

    # 杀掉Monkey进程
    def killMonkeyThread(self):
        try:
            monkeyPid = []
            grepMonkey = subprocess.Popen(self.grepMonkey, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE).stdout.readlines()
            if len(grepMonkey) != 0:
                kk = str(grepMonkey[0]).split(" ")
                for i in range(len(kk)):
                    if kk[i] != "":
                        monkeyPid.append(kk[i])
                killMonkey = 'adb shell "kill %s"' % monkeyPid[1]
                os.system(killMonkey)
                logger.info("Successfully kill monkey process：%s"%(monkeyPid[1]))
            else:
                logger.info("No monkey program is running the skip kill process")
        except Exception as IOError:
            logger.info(IOError)

    def checklocal(self):
        """
        检查本地是否安装包名
        :return:
        """
        result = []
        devices = Adb.check_devices_status()
        if len(devices)==1:
            packageName = subprocess.getstatusoutput('adb shell pm list packages "| grep %s"' % (self.package))[1][8:].strip('\r\n')
            result.append(packageName)
        elif len(devices)>1:
            for i in range(len(devices)):
                packageName = subprocess.getstatusoutput('adb -s %s shell pm list packages "| grep %s"' % (devices[i], self.package))[1][8:].strip('\r\n')
                result.append(packageName)
        return result

    def checkInstall(self):
        """
        安装测试APK
        :return:
        """
        packages = self.checklocal()
        devices = Adb.check_devices_status()
        if len(devices) == 1:
            installInfo = subprocess.getstatusoutput('adb install -r %s' % (self.apkpath))
            if 'Success' in installInfo[1]:
                logger.info("设备：%s 安装%s成功" % (devices, self.apkpath))
            else:
                logger.error("设备：%s 安装失败，错误信息：%s" % (devices, installInfo[1]))
        elif len(devices) > 1:
            for i in range(len(devices)):
                installInfo = subprocess.getstatusoutput('adb -s %s install -r %s' % (devices[i], self.apkpath))
                if 'Success' in installInfo[1]:
                    logger.info("设备：%s 安装%s成功" % (devices[i], self.apkpath))
                else:
                    logger.error("设备：%s 安装失败，错误信息：%s" % (devices[i], installInfo[1]))

    def coverPage(self):
        """
        通过白名单机制进行二次封装Monkey自定义Activity
        :return:
        """
        whitelist = []
        content = os.popen('adb shell dumpsys activity  |findstr "mResumedActivity" ').read()  # 读取当前页面
        activity = re.compile(r'com.*').findall(content)[0].split(' ')[0]
        for line in open(self.whiteapath):
            whitelist.append(line.strip())
        if activity not in whitelist:
            logger.info('当前运行窗口：%s' % (activity))
            start = subprocess.getstatusoutput(
                'adb shell am start -n %s/%s' % (self.package, self.mainactivity))
            logger.info("成功返回主窗口：%s" % (start[1]))
        else:
            logger.info("当前位于：%s不需要跳转！！！" % (activity))

    def sleepTime(self,hour, min, sec):
        return hour * 3600 + min * 60 + sec

    def logMonitor(self):
        """
        日志监控
        :return:
        """
        os.popen("adb shell ''mkdir %s''" % (self.AndroidFile))

        content = os.popen(r'adb logcat -b "crash" -f aaa.log')
        print(content)



    def initenviron(self):
        """
        复位状态栏
        :return:
        """
        devices = Adb.check_devices_status()
        if len(devices) == 1:
            os.popen('adb shell settings put global policy_control immersive.full=*')
            os.popen('adb shell wm overscan 0,0,0,000')
        else:
            for i in range(len(devices)):
                os.popen('adb -s %s shell settings put global policy_control immersive.full=*' % (devices[i]))
                os.popen('adb -s %s shell wm overscan 0,0,0,000' % (devices[i]))

    def startMonkey(self):
        """
        部署生态的Monkey
        :return:
        """
        if str(self.killMonkey)!="1":
            pass
        else:
            self.killMonkeyThread()
            self.initenviron()
            # self.checkInstall()
            # self.logMonitor()
            # os.popen(r'adb shell screenrecord %s%s.mp4' % (self.AndroidFile, self.Today))
            # second = Monkey().sleepTime(0, 0, 5)
            # while 1 == 1:
            #     time.sleep(second)
            #     Monkey().coverPage()

if __name__ == '__main__':
    Monkey().startMonkey()
