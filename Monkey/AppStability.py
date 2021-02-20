# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： AppStability.py
# Author : YuYanQing
# Desc: Monkey脚本
# Date： 2020/1:11 10:57
'''
import linecache
import re,os,time
import subprocess

from BaseSetting import AbsPath
from Logger.GlobalLog import Logger
from Utils.ConfigParser import  IniHandle
from Utils.DirTools import  DocProcess
from Utils.AdbTools import AdbManage
Adb = AdbManage()
logger = Logger.write_log()
getpwd =DocProcess.getSuperiorDir()
class Monkey():
    def __init__(self,device=None):
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
        if device is None:
            devices = re.findall('\n(.+?)\t', subprocess.getstatusoutput("adb devices")[1])
            self.devices = devices[0]
        else:
            self.devices = device
        self.send = int(time.time())
        self.resultPath =r"../Result/"
        self.adb = "adb -s %s "%(self.devices)
        self.shell = "adb -s %s shell"%(self.devices)
        self.today = time.strftime("%Y%m%d%H%M%S").replace("4","6")
        self.package = IniHandle.optValue(node="Monkey_Test",key="package")
        self.logPath =r"/sdcard/AutoMonkey/%s/"%(self.package)
        self.AutoMonkeyPath =r"%sAutoMonkey"%(self.resultPath)
        # Monkey [option] <count> 1>default.txt 2>error.txt
        self.default = "%s%s-default.log"%(self.logPath,self.today)
        self.error = "%s%s-error.log"%(self.logPath,self.today)
        self.allCrashLog = r"%s%s-Crash.log"%(self.logPath,self.today)
        self.apkpath =os.path.join(getpwd,IniHandle.optValue(node="Monkey_Test",key="apkpath"))
        # 包名及主activity
        self.mactivity = IniHandle.optValue(node="Monkey_Test",key="mainactivity")
        # commodMonkey 命令
        self.grepMonkey = IniHandle.optValue(node="Monkey_Test",key="grepMonkey")
        self.operation = IniHandle.optValue(node="Monkey_Test",key="operation")
        self.throttle = IniHandle.optValue(node="Monkey_Test",key="throttle")
        self.ignore =  IniHandle.optValue(node="Monkey_Test",key="ignore")
        self.loglevel = IniHandle.optValue(node="Monkey_Test",key="loglevel")
        self.count = IniHandle.optValue(node="Monkey_Test",key="count")
        self.commod = ('%s monkey -p %s %s %s %s %s -s %s %s '%(self.shell,self.package,self.operation,self.throttle,self.ignore,self.loglevel,self.send,self.count))
        self.time =IniHandle.optValue(node="Monkey_Test",key="time")
        self.out_put = " 1> %s 2>%s"%(self.default,self.error)
        self.sd_path = r"/data/local/tmp"
        self.local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def checklocal(self):
        """
        检查本地是否安装包名
        :return:
        """
        packageName = subprocess.getstatusoutput('%s pm list packages "| grep %s"' % (self.shell,self.package))[1][8:].strip('\r\n')
        return packageName

    def grepEnterActivity(self, package):
        """
        过滤指定包名的一些信息及主入口
        :return:
        """
        content = os.popen('%s dumpsys package %s "' % (self.shell, package))  # 读取当前页面
        lines = content.readlines()
        index = 0
        for line in lines:
            index += 1
            if "Non-Data Actions:" in line.strip():
                activity = lines[index + 1].strip().split(" ")[1]
                print("捕捉到主入口：%s" % (activity))
                return activity

    def setBlacklist(self):
        """
        过滤黑名单日志
        :return:
        """
        temp = subprocess.getstatusoutput('%s pm list packages' %(self.shell))[1].split("package:")
        index = 0
        packages = []
        while index<len(temp):
            if len(temp[index]) >1 :
                packages.append(temp[index].strip())
            index +=1
        packages.remove(self.package); # 移除需要运行的软件
        logger.info("检索到当前设备：%s本地已安装了%s个软件,分别为：%s"%(self.devices,len(packages),packages))
        # 写入到本地
        file_path = os.path.join(AbsPath,r"Config/blacklist.txt")
        with open(file_path,"w") as file:
            for i in range(len(packages)):
                file.write("%s\n"%(packages[i]))
        print("%s push %s %s"%(self.shell,file_path,self.sd_path))
        subprocess.getstatusoutput("%s push %s %s"%(self.adb,file_path,self.sd_path))
        return file_path

    def setWhitelist(self):
        """
        设置白名单
        :return:
        """
        file_path = os.path.join(AbsPath, r"Config/whitelist.txt")
        subprocess.getstatusoutput("%s push %s %s" % (self.adb,file_path,self.sd_path))
        return file_path

    def killMonkeyThread(self):
        """
        结束掉Monkey进程
        :return:
        """
        try:
            monkeyPid = []
            monkey = subprocess.Popen(self.grepMonkey, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE).stdout.readlines()
            # [b'shell        29622 29127 4135336  56328 futex_wait_queue_me 0 S com.android.commands.monkey\r\n']
            if len(monkey) != 0:
                port = str(monkey[0]).split(" ")
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
        clearLog = "%s logcat -b all -c" % (self.shell)  #  加上-b all 修复failed to clear the 'main' log
        grepCrash ='adb logcat -b "crash" -f %s' % (self.allCrashLog)
        clearLogInfo =  os.popen(clearLog)
        clearLogInfo.close()
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
        logger.info("%s"%(str(coverPage[1])))

    def initFile(self):
        """
        初始化文件(发现6系统的删除了文件后需要重启设备才看到，bug记录下)
        :return:
        """
        logger.info("初始化日志存储位置：\nCrash：%s\nMonkey：[%s,%s]" % (self.allCrashLog, self.default,self.error))
        os.popen("%s ''rm -rf %s''" % (self.shell, self.logPath))
        os.popen("%s ''mkdir -p %s''" % (self.shell, self.logPath))

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

    def forceApp(self, package):
        """
        退出应用
        :return: quit_app
        """
        stop = subprocess.getstatusoutput("%s am force-stop %s " % (self.shell, package))
        logger.info("%s am force-stop %s " % (self.shell, package))
        logger.info("已成功退出%s " % (package))
        return stop

    def startMonkey(self,policy=None,astrict=None):
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
        self.forceApp(self.package)
        if astrict == "white":
            file_path = self.setWhitelist()
            commod = self.commod +"" +"--pkg-whitelist-file "+file_path+ self.out_put
        elif astrict == "black":
            file_path = self.setBlacklist()
            print(file_path)
            commod = self.commod +"" +" --pkg-blacklist-file "+file_path+ self.out_put
        else:
            commod = self.commod + "" + self.out_put
        subprocess.Popen(commod)
        self.grepCrashLog()
        # while True:
        #     time.sleep(int(self.time))
        #     self.startActivity()
        file_path = os.path.join(AbsPath, r"Result/%s/%s-monkey-cmd.txt"%(self.local_date,self.today))
        with open(file_path,"w") as file:
            file.write(commod)
        logger.info("Monkey已成功运行 %s"%(commod))

    def getRelust(self):
        """
        复位状态栏/导出结果
        :return:
        """
        self.killMonkeyThread()
        self.coverSetting()
        self.pullFile()

    def grepError(self,filePath):
        try:
            tempPath = "%s.grep"%(filePath)
            if os.path.exists(filePath):
                logger.info("最终拼接路径：%s,输出路径：%s"%(filePath,tempPath))
                with open(filePath,"r") as file,open(tempPath,"w") as res:
                    lines = file.readlines()
                    index = 0
                    count = 0
                    rows = []
                    for line in lines:
                        index += 1
                        if "crash" in line:
                            count +=1
                            startStr = linecache.getline(filePath, index)
                            rows.append(index)
                            maxIndex = index + 35
                            for i in range(index,maxIndex):
                                connetStr = linecache.getline(filePath, i)
                                res.write(connetStr)
                    logger.info("Bug数量：%s   行数：%s"%(count,rows))
        except FileNotFoundError:
            logger.error('无法打开指定的文件！！！')
        except LookupError:
            logger.error('指定了未知的编码！！！')
        except UnicodeDecodeError:
            logger.error('读取文件时解码错误！！！')

    def restartMonkey(self,filepath):
        """
        重跑Monkey
        :return:
        """
        self.initFile()
        self.killMonkeyThread()
        self.forceApp(self.package)
        with open(filepath,"r") as file:
            commod = file.readline()
        file.close()
        subprocess.Popen(commod)
        self.grepCrashLog()

if __name__ == '__main__':
    # Monkey().startMonkey("full")
    # Monkey("538640ed").getRelust()
    # Monkey().killMonkeyThread()
    # Monkey().initFile()
    # Monkey("538640ed").grepError(r"D:\Work_Spaces\PyCharm_Project\AutoFramework\Result\AutoMonkey\20200109-Crash.log")
    # Monkey().grep_blacklist()
    Monkey().startMonkey(astrict="white")
    # Monkey().restartMonkey(r"E:\WorkSpace\PycharmProjects\AutoFramework\Result\2021-02-20\20210220170135-monkey-cmd.txt")
    # Monkey().grepEnterActivity("com.tencent.now")