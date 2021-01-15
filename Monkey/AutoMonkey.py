# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： AppStability.py
# Author : v_yanqyu
# Desc: Monkey脚本 傻瓜版
# Date： 2020/1:11 10:57
'''
import linecache
import re,os,time
import subprocess
import configparser
class Monkey():
    def __init__(self,device=None,filepath=None):
        """
        :param device:  设备ID
        :param today 当前时间
        :param send 种子数
        :param logPath 安卓的总存储目录
        :param tempPath 临时路径（mkdir -p 不生效）
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
        try:
            if filepath is None:
                filepath = r'../Config/config.ini'
                print(filepath)
            conf = configparser.ConfigParser()
            conf.read(filepath, encoding="utf-8")
        except Exception as FileNotFoundError:
            print("文件读取失败，请检查%s是否存在,错误信息：%s" % (filepath,FileNotFoundError))
        # 文件读取及存储的路径
        if device is None:
            devices = re.findall('\n(.+?)\t', subprocess.getstatusoutput("adb devices")[1])
            self.devices = devices[0]
        else:
            self.devices = device
        print("连接设备：%s"%(self.devices))
        self.send = int(time.time())
        self.resultPath = r"../Result/"
        self.shell = "adb -s %s shell" % (self.devices)
        self.today = time.strftime("%Y%m%d%H%M%S").replace("4", "6")
        self.package = conf.get("Monkey_Test", "package")
        self.logPath = r"/sdcard/AutoMonkey/%s/" % (self.package)
        self.AutoMonkeyPath = r"%sAutoMonkey" % (self.resultPath)
        self.default = "%s%s-default.log" % (self.logPath, self.today)
        self.error = "%s%s-error.log" % (self.logPath, self.today)
        self.allCrashLog = r"%s%s-Crash.log" % (self.logPath, self.today)
        # 包名及主activity
        self.mactivity = conf.get("Monkey_Test", "mainactivity")
        # commodMonkey 命令
        self.grepMonkey = conf.get("Monkey_Test", "grepMonkey")
        self.operation = conf.get("Monkey_Test", "operation")
        self.throttle = conf.get("Monkey_Test", "throttle")
        self.ignore = conf.get("Monkey_Test", "ignore")
        self.loglevel = conf.get("Monkey_Test", "loglevel")
        self.count = conf.get("Monkey_Test", "count")
        self.commod = (r'%s monkey -p %s %s %s %s %s -s %s %s " 1> %s 2>%s"' % (self.shell, self.package, self.operation, self.throttle, self.ignore, self.loglevel, self.send, self.count,self.default, self.error))
        self.time = conf.get("Monkey_Test", "time")
        self.policy =conf.get("Monkey_Test", "policy")

    def checklocal(self):
        """
        检查本地是否安装包名
        :return:
        """
        packageName = subprocess.getstatusoutput('%s pm list packages "| grep %s"' % (self.shell,self.package))[1][8:].strip('\r\n')
        return packageName

    def uninstallApk(self,apkpath):
        if self.checklocal() !='':
            uninstall = subprocess.getstatusoutput('adb -s %s uninstall %s' % (self.devices, apkpath))
            if 'Success' in uninstall[1]:
                print("设备：%s 卸载%s成功" % (self.devices, apkpath))
                return True
            else:
                print("设备：%s 卸载失败，错误信息：%s" % (self.devices, uninstall[1] ))

    def installApk(self,apkpath):
        """
        安装测试APK
        :return:
        """
        install = subprocess.getstatusoutput('adb -s %s install -r %s' % (self.devices, apkpath))
        if 'Success' in install[1]:
            print("设备：%s 安装%s成功" % (self.devices, apkpath))
            return True
        else:
            print("设备：%s 安装失败，错误信息：%s" % (self.devices, install[1]))

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
                print("Successfully kill monkey process：%s"%(monkeyPid[1]))
            else:
                print("No monkey program is running the skip kill process")
        except Exception as IOError:
            print(IOError)

    def grepActivity(self):
        """
        过滤当前Actviity
        :return:
        """
        content = os.popen('%s dumpsys activity  |findstr "mResumedActivity" '%(self.shell)).read()  # 读取当前页面
        activity = re.compile(r'com.*').findall(content)[0].split(' ')[0]
        print("检索到当前Activity：%s"%(activity))
        return activity

    def grepCrashLog(self):
        """
        监听crash日志
        :return:
        """
        grepCrash ='adb logcat -b "crash" -f %s' % (self.allCrashLog)
        subprocess.Popen(grepCrash)

    def startActivity(self):
        """
        跳转Activity
        :return:
        """
        coverPage = subprocess.getstatusoutput('%s am start -n %s' % (self.shell,self.mactivity))
        print("%s"%(str(coverPage[1])))

    def initFile(self):
        """
        初始化文件(发现6系统的删除了文件后需要重启设备才看到，bug记录下)
        :return:
        """
        print("初始化日志存储位置：\nCrash：%s\nMonkey：[%s,%s]" % (self.allCrashLog, self.default,self.error))
        os.popen("%s ''rm -rf %s''" % (self.shell, self.logPath))
        os.popen("%s ''mkdir -p %s''" % (self.shell, self.logPath))

    def pullFile(self):
        """
        将Phone设备中的运行日志导出至PC
        :return:
        """
        pullFile =subprocess.getoutput("adb -s  %s pull %s "%(self.devices,self.logPath))
        print("adb Pull %s"%(pullFile))

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
        print("%s am force-stop %s " % (self.shell, package))
        print("已成功退出%s " % (package))
        return stop

    def startMonkey(self):
        """
        首次启动Monkey
        :param policy:  是否需要设置底部键盘栏及状态栏隐藏
        :return:
        """
        policy = self.policy
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
        print("Monkey最终的运行参数：%s"%(self.commod))
        subprocess.Popen(self.commod)
        self.grepCrashLog()

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
                print("最终拼接路径：%s,输出路径：%s"%(filePath,tempPath))
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
                    print("Bug数量：%s   行数：%s"%(count,rows))
        except FileNotFoundError:
            print('无法打开指定的文件！！！')
        except LookupError:
            print('指定了未知的编码！！！')
        except UnicodeDecodeError:
            print('读取文件时解码错误！！！')

    def restartMonkey(self,send):
        """
        重跑Monkey
        :return:
        """
        self.initFile()
        self.killMonkeyThread()
        self.forceApp(self.package)
        default = "%s%s-restart-default.log"%(self.logPath,send)
        error = "%s%s-restart-error.log"%(self.logPath,send)
        recommod = ('%s monkey -p %s %s %s %s %s -s %s %s " 1> %s 2>%s"'%(self.shell,self.package,self.operation,self.throttle,self.ignore,self.loglevel,send,self.count,default,error))
        subprocess.Popen(recommod)
        self.grepCrashLog()


if __name__ == '__main__':
    try:
        while True:
            Code = input("FileName： AppStability.py  Desc: Monkey脚本 \n"
                         "Author : v_yanqyu Email：mryu168@163.com\n"
                         "输入1---启动Monkey (设备Id,参数配置,导航栏：full(全部隐藏),status(只隐藏导航栏),invent(只隐藏华为等系列底部软按钮))\n"
                         "输入2---停止Monkey \n"
                         "输入3---导出日志 (会在根目录下Pull)\n"
                         "输入5---过滤Crash的数量 （需要文本的路径）\n"
                         "输入6---监听Crash日志\n"
                         "输入7---安装Apk\n"
                         "输入8---卸载Apk\n"
                         "输入9---复位手机设置(导航栏及其它的配置)\n"
                         "输入10---过滤指定包名的主Activity\n"
                         "输入11---过滤当前Activity\n"
                         "输入12---初始化文件夹\n"
                         "输入13---重跑Monkkey\n"
                         "请输入需要执行的脚本序列号：")
            print("%s" % (Code))
            if Code == "1":
                Monkey().startMonkey()
            elif Code == "2":
                Monkey().killMonkeyThread()
            elif Code == "3":
                Monkey().getRelust()
            elif Code == "5":
                Monkey().grepError(input("需要过滤Crash的Txt文本路径："))
            elif Code == "6":
                Monkey().grepCrashLog()
            elif Code == "7":
                Monkey().installApk(input("请输入安装包完整路径："))
            elif Code == "8":
                Monkey().uninstallApk(input("请输入卸载的包名："))
            elif Code == "9":
                Monkey().coverSetting()
            elif Code == "10":
                Monkey().grepEnterActivity(input("请输入需要过滤的package："))
            elif Code == "11":
                Monkey().grepActivity()
            elif Code == "12":
                Monkey().initFile()
            elif Code == "13":
                Monkey().restartMonkey(input("请输入Send种子数："))
            else:
                print("暂不支持更多功能")
    except Exception as error:
        print(error)
