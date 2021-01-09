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
    def __init__(self,device):
        """
        :param device:  设备ID
        :param today 当前时间
        :param send 种子数
        :param logPath 安卓的总存储目录
        :param tempFile 临时文件
        :param allMonkeyLog 所有的日志文件
        :param allcrashLog crash日志文件路径

        :param package 测试包名
        :param mactivity 主窗口

        :param grepMonkey adb shell "ps | grep monkey"
        :param apkpath 安装包路径
        :param operation Monkey事件参数
        :param throttle  事件间隔时间
        :param ignore    忽略事件
        :param loglevel  日志等级
        :param count 运行次数
        :param commod 将monkey指定的参数都统一加一起
        """
        # 文件读取及存储的路径
        self.devices = device
        self.shell = "adb -s %s shell"%(device)
        self.send = int(time.time())
        self.today = time.strftime("%Y%m%d%H%M%S").replace("4","6")
        self.logPath =r"/sdcard/AutoMonkey/"
        self.resultPath =r"../Result/"
        self.AutoMonkeyPath =r"%sAutoMonkey"%(self.resultPath)
        self.tempFile = r"../Result/%s-AllMonkey.log"%(self.today)
        self.allMonkeyLog = "%s%s-AllMonkey.log"%(self.logPath,self.today)
        self.allCrashLog = r"%s%s-Crash.log"%(self.logPath,self.today)
        self.apkpath =os.path.join(getpwd,IniHandle.optValue(node="Monkey_Test",key="apkpath"))
        # 包名及主activity
        self.package = IniHandle.optValue(node="Monkey_Test",key="package")
        self.mactivity = IniHandle.optValue(node="Monkey_Test",key="mainactivity")
        # commodMonkey 命令
        self.grepMonkey = IniHandle.optValue(node="Monkey_Test",key="grepMonkey")
        self.operation = IniHandle.optValue(node="Monkey_Test",key="operation")
        self.throttle = IniHandle.optValue(node="Monkey_Test",key="throttle")
        self.ignore =  IniHandle.optValue(node="Monkey_Test",key="ignore")
        self.loglevel = IniHandle.optValue(node="Monkey_Test",key="loglevel")
        self.count = IniHandle.optValue(node="Monkey_Test",key="count")
        self.commod = ('%s monkey -p %s %s %s %s %s -s %s %s "> %s"'%(self.shell,self.package,self.operation,self.throttle,self.ignore,self.loglevel,self.send,self.count,self.allMonkeyLog))
        self.keyword = IniHandle.optValue(node="Monkey_Test",key="keyword").split(",")

    def checklocal(self):
        """
        检查本地是否安装包名
        :return:
        """
        packageName = subprocess.getstatusoutput('%s pm list packages "| grep %s"' % (self.shell,self.package))[1][8:].strip('\r\n')
        return packageName

    def installApk(self):
        """
        安装测试APK
        :return:
        """
        installInfo = subprocess.getstatusoutput('adb -s %s install -r %s' % (self.devices, self.apkpath))
        if 'Success' in installInfo[1]:
            logger.info("设备：%s 安装%s成功" % (self.devices, self.apkpath))
            return True
        else:
            logger.error("设备：%s 安装失败，错误信息：%s" % (self.devices, installInfo[1]))

    def killMonkeyThread(self):
        """
        结束掉Monkey进程
        :return:
        """
        try:
            monkeyPid = []
            grepMonkey = subprocess.Popen(self.grepMonkey, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE).stdout.readlines()
            # [b'shell        29622 29127 4135336  56328 futex_wait_queue_me 0 S com.android.commands.monkey\r\n']
            if len(grepMonkey) != 0:
                port = str(grepMonkey[0]).split(" ")
                for i in range(len(port)):
                    if port[i] != "":
                        monkeyPid.append(port[i])
                killMonkey = '%s "kill %s"' % (self.shell,monkeyPid[1])
                os.popen(killMonkey)
                logger.info("Successfully kill monkey process：%s"%(monkeyPid[1]))
            else:
                logger.info("No monkey program is running the skip kill process")
        except Exception as IOError:
            logger.info(IOError)

    def grepActivity(self):
        """
        过滤当前Actviity
        :return:
        """
        content = os.popen('%s dumpsys activity  |findstr "mResumedActivity" '%(self.shell)).read()  # 读取当前页面
        activity = re.compile(r'com.*').findall(content)[0].split(' ')[0]
        return activity

    def grepCrashLog(self):
        """
        监听crash日志
        :return:
        """
        clearLog = "%s logcat -c " % (self.shell)
        grepCrash ='adb logcat -b "crash" -f %s' % (self.allCrashLog)
        clearLogInfo = os.popen(clearLog)
        logger.info(clearLog)
        if clearLogInfo == "1":
            logger.error("%s"%(clearLogInfo))
        else:
            logger.info("已成功清理掉之前的日志......")
        logger.info(grepCrash)
        subprocess.Popen(grepCrash)

    def startActivity(self):
        """
        跳转Activity
        :return:
        """
        coverPage = subprocess.getstatusoutput('%s am start -n %s' % (self.shell,self.mactivity))
        error = re.findall(r'not.*', str(coverPage[1]))
        if error !=[]:
            logger.info("跳转Activity失败ErrorInfo：\n%s"%(str(coverPage[1])))
        else :
            logger.info("成功跳转至Activity：%s"%(self.mactivity))

    def initFile(self):
        """
        初始化文件
        :return:
        """
        logger.info("初始化日志存储位置：\nCrash：%s\nMonkey：%s" % (self.allCrashLog, self.allMonkeyLog))
        os.popen("%s ''rm -rf %s''" % (self.shell, self.logPath))
        os.popen("%s ''mkdir %s''" % (self.shell, self.logPath))

    def pullFile(self):
        """
        将Phone设备中的运行日志导出至PC
        :return:
        """
        pullFile =subprocess.getoutput("adb -s  %s pull %s %s"%(self.devices,self.logPath,self.resultPath))
        logger.info("adb Pull %s"%(pullFile))

    def coverSetting(self):
        """
        复位手机设置(导航栏及其它的配置)
        :return:
        """
        subprocess.Popen("%s settings put global policy_control null" % (self.shell))
        os.popen('%s wm overscan 0,0,0,0' % (self.shell))

    def startMonkey(self,policy=None):
        """
        首次启动Monkey
        :param policy:  是否需要设置底部键盘栏及状态栏隐藏
        :return:
        """
        if policy =='full':
            subprocess.Popen("%s settings put global policy_control immersive.full=*"%(self.shell))
        elif policy =='status':
            subprocess.Popen("%s settings put global policy_control immersive.status=*"%(self.shell))
        elif policy =='invent':
            subprocess.Popen("%s settings put global policy_control immersive.navigation=*"%(self.shell))
        else:
            subprocess.Popen("%s settings put global policy_control null"%(self.shell))
        self.initFile()
        self.killMonkeyThread()
        logger.info("Monkey最终的运行参数：%s"%(self.commod))
        subprocess.Popen(self.commod)
        self.grepCrashLog()

    def getRelust(self):
        """
        复位状态栏/导出结果
        :return:
        """
        self.killMonkeyThread()
        self.coverSetting()
        self.pullFile()

    def grepError(self):
        filePath = []
        for dirpath, dirnames, filenames in os.walk(self.AutoMonkeyPath):
            logger.info("检索到路径：%s下有%s个文件 %s"%(dirpath,len(filenames),filenames))
            for i in range(len(filenames)):
                filePath.append("%s/%s"%(dirpath,filenames[i]))
            logger.info("拼接路径：%s"%(filePath))
            for i in range(len(filePath)):
                with open(filePath[i]) as file:
                    for line in file.readlines():
                        line = line.strip('\n')

if __name__ == '__main__':
    # Monkey("D8H6R19630008844").startMonkey()
    Monkey("D8H6R19630008844").grepError()

