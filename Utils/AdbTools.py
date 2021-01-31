# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： AdbTools.py
# Author : v_yanqyu
# Desc: Adb工具类
# Date： 2020/9/6 18:56
'''
import linecache
import os,re
import platform,datetime
import subprocess
from Logger.GlobalLog import Logger
from Utils import DirTools
logger = Logger.write_log()#调用日志模块

class AdbManage(object):
    def __init__(self,devicesId=None):
        """
        初始化设备id
        Traceback (most recent call last):（报错异常原因 设备未找到）
            adb = AdbManage()
            self.devicesId = self.getDevices()[0]
        TypeError: 'bool' object is not subscriptable
        """
        if devicesId ==None:
            self.devicesId = self.getDevices()[0]
        else:
            self.devicesId = devicesId
        self.commod = "adb -s %s"%(self.devicesId)

    def checkFiltered(self):
        '''
        检查本地环境是Win还是Linux
        :return:
        '''
        if platform.system().lower() == 'windows':
            logger.info("检测到本地为Windows环境")
            filter = "findstr"
        elif platform.system().lower() == 'linux':
            logger.info("检测到本地为Linux环境")
            filter = "gerp"
        else:
            logger.error("不支持该系统环境下运行！！！")
        return filter

    def checklocalFile(self):
        """
        检查本地文件是否存在
        :param superiordirectory:上级目录
        :param general_file:拼接后的APK包存储目录
        :return apk_filepath：拼接后的安卓包完整目录
        """
        apklist = []
        superiordirectory = DirTools.DocProcess().getSuperiorDir()
        # logger.info("上级所在目录为：{}".format(superiordirectory))
        general_file = superiordirectory + "\APKPath"
        # logger.info("APK存储路径：{}".format(general_file))
        try:
            path = os.listdir(general_file)
            for i in range(0,len(path)):
                for file_path in os.listdir(general_file):
                    apk_filepath = general_file + "\\" + file_path
                    apklist.append(apk_filepath)
            return apklist
        except Exception as TypeError:
            logger.error(TypeError)

    def getSdkPath(self):
        """
        检查adb 判断是否设置环境变量ANDROID_HOME
        :param adb_info adb环境信息
        :param adb_status 状态
        :return: True：环境正常 、False：环境异常
        """
        adb_info = subprocess.getstatusoutput("adb version")
        adb_status = adb_info[0]
        if adb_status == "1" :
            return False
        else:
            # logger.info("\n%s"%(adb_info[1]))
            return True

    def adb(self,args):
        """
        adb命令
        :return:
        """
        adb = "adb -s %s %s"%(self.devicesId,str(args)) # 由于有些命令不能跟shell
        logger.info("%s"%(adb))

    def shell(self,args):
        """
        adb shell 命令
        :param args:
        :return:
        """
        shell = "adb -s %s shell %s"%(self.devicesId,str(args))
        logger.info("%s"%(shell))

    def getDevices(self):
        """
        检查设备是否连接成功，如果成功返回Device_Nmae，否则返回False
        :param devices_info：CMD输入
        :return devices：设备ID
        """
        adb_info = self.getSdkPath()
        if adb_info == True:
            devices = re.findall('\n(.+?)\t', subprocess.getstatusoutput("adb devices")[1])
            if devices != []:
                # logger.info("设备连接成功%s" % (devices))
                return devices
            else:
                logger.error("请检查目标设备是否与主机连接成功！！！")
                return False
        else:
            logger.error("本地没有配置Android_SDK环境！！！")

    def getRootStatus(self):
        """
        检查设备ROOT状态
        :param devices: 设备ID
        :param root_info：root检测用的
        :return:True：() Flase：(3, 'E must be run as root')
        """
        root = subprocess.getstatusoutput("%s shell remount" % (self.commod))
        status ,message = root[0],root[1]
        if status == 0 and message == "remount succeeded":
            logger.info("设备ID：%sROOT授权成功，%s" % (self.devicesId, message))
            return True
        else:
            logger.error("设备ID：%s没有ROOT授权，%s" % (self.devicesId, message))
            return False

    def checklocal(self,package):
        """
        检查本地是否安装包名
        :return:
        """
        packageName = subprocess.getstatusoutput('%s shell pm list packages "| grep %s"' % (self.commod,package))[1][8:].strip('\r\n')
        return packageName

    def uninstallApk(self,apkPath):
        logger.info('%s shell uninstall %s' % (self.commod, apkPath))
        uninstall = subprocess.getstatusoutput('%s shell uninstall %s' % (self.commod, apkPath))
        status,message = uninstall[0],uninstall[1]
        if status == 0 or "Success" in message:
            logger.info("设备：%s 卸载%s成功" % (self.devicesId, self.apkpath))
            return True
        else:
            logger.error("设备：%s 卸载失败，错误信息：%s" % (self.devicesId, message ))

    def installApk(self, apkPath):
        """
        安装apk文件
        :param 安装包路径
        :return:
        """
        logger.info("%s install %s"%(self.commod,apkPath))
        insatll = subprocess.getstatusoutput("%s install %s"%(self.commod,apkPath))
        status,message = insatll[0],insatll[1]
        head,tail = os.path.split(apkPath)
        if status == 0 or "Success" in message:
            logger.info("设备：%s 安装 %s成功" % (self.devicesId, tail))
        elif "Failure [-200]" in message:
            logger.info("设备：%s 取消安装！！！" % (self.devicesId))
        else:
            logger.info("设备：%s 安装失败,ErrorInfo" % (self.devicesId, message))

    def clearPackage(self,package):
        """
        清理数据缓存
        :param package: 包名
        :return:
        """
        logger.info("当前终端ID：%s，清除数据过程中请勿移除USB连接！！！" % (self.devicesId))
        clear = subprocess.getstatusoutput('adb -s %s shell pm clear %s' % (self.devicesId, package))
        status,message = clear[0],clear[1]
        if status == 0 or "Success" in message:
            logger.info("设备：%s清除数据成功" % (self.devicesId))
        else:
            logger.error("设备：%s清除数据失败,ErrorInfo：%s" % (self.devicesId,message))

    def getIpconfig(self):
        """
        获取已连接的手机WIFI_IP
        :param ipconfig：wlan0基本Ip信息
        :return ip
        """
        ipconfig = os.popen("%s shell ifconfig wlan0" % (self.commod)).read().replace(" ", "")  # window下使用findstr
        if "wlan0:Cannotassignrequestedaddress" in ipconfig:
            logger.error("获取%s设备WIFI_IP失败,请检查是否连接网络！！！%s" % (self.devicesId, ipconfig))
        else:
            ipv4 = re.findall(r'\binetaddr:\S*?Bcast\b', ipconfig)[0].rsplit(":")[1].rsplit("Bcast")[0]
            ipv6 = re.findall(r'\binet6addr:\S*?Scope\b', ipconfig)[0].rsplit("inet6addr:")[1].rsplit("Scope")[0]
            logger.info("检索到设备%s当前IPV4：%s,IPV6：%s" % (self.devicesId, ipv4, ipv6))
        return ipv4, ipv6

    def dump_xml(self,source, filename):
        """
        dump apk xml文件
        :return:
        """
        return os.popen('%s shell aapt dump xmlstrings %s %s'%(self.commod) % (source, filename))

    def uiautomator_dump(self):
        """
        获取屏幕uiautomator xml文件
        :return:
        """
        return  os.popen("%s shell uiautomator dump "%(self.commod)[1].strip())

    def getMacAddress(self):
        """
        获取设备MAC地址
        :return:
        """
        mac = subprocess.getstatusoutput("%s shell 'cat /sys/class/net/wlan0/address'"%(self.commod))
        print(mac)

    def remoteConnectdev(self,ipv4):
        """
        远程连接设备
        :param ipv4:
        :return:
        """
        check_ip = os.popen("ping {}".format(ipv4)).read()
        restart_adb = os.popen("adb tcpip 5555").read()
        str = "Ping 请求找不到主机 None。请检查该名称，然后重试。"
        if str == check_ip or restart_adb == "":
            logger.error("adb tcpip模式重启adb失败%s" % (check_ip))
        else:
            logger.info("adb tcpip模式重启adb成功！！！")
            connect = os.popen("adb connect {}".format(ipv4)).read()
            logger.info(connect)
        return check_ip

    def grepEnterActivity(self,package):
        """
        过滤指定包名的一些信息及主入口
        :return:
        """
        content = os.popen('%s shell dumpsys package %s "'%(self.commod,package)) # 读取当前页面
        lines = content.readlines()
        index = 0
        for line in lines:
            index += 1
            if "Non-Data Actions:" in line.strip():
                activity = lines[index+1].strip().split(" ")[1]
                logger.info("捕捉到主入口：%s"%(activity))
                return activity

    def grepActivity(self):
        """
        过滤当前Actviity
        :return:
        """
        content = os.popen('%s shell dumpsys activity  |findstr "mResumedActivity"'%(self.commod)).read()  # 读取当前页面
        activity = re.compile(r'com.*').findall(content)[0].split(' ')[0]
        logger.info("获取到当前运行的Activity：%s"%(activity))
        return activity

    def getBatteryInfo(self):
        '''
        获取Android手机电池电量
          status: 1            #电池状态：2：充电状态 ，其他数字为非充电状态
          health: 2            #电池健康状态：只有数字2表示good
          present: true        #电池是否安装在机身
          level: 55            #电量: 百分比
          scale: 100
          voltage: 3977         #电池电压
          current now: -335232  #电流值，负数表示正在充电
          temperature: 335      #电池温度，单位是0.1摄氏度
          technology: Li-poly    #电池种类=
        '''
        battery = os.popen("%s shell dumpsys battery" % (self.commod)).read().split("\n")  # window下使用findstr
        batterystatus = battery[7]
        batterylevel = battery[10]
        logger.info("成功获取到{}设备电池信息：{},{}".format(self.devicesId, batterystatus, batterylevel))
        return battery, batterystatus, batterylevel

    def createFile(self, method, filePath):
        """
        创建目录
        :param  split_path：清理文件尾椎
        :param  mkdir_msg：运行后返回的结果集 1代表False、0代表True
        :param  method: 调用的方法元素、mkdir：创建文件、 touch：创建文件夹
        :param  make_dir：创建文件夹、且会携带返回结果集
        :param  touch_file: 创建文件
        """
        head, tail = os.path.split(filePath)
        # 清理文件尾椎例如：/sdcard/maketest/AutoFramework.text 自动过滤掉为/sdcard/maketest/AutoFramework
        mkdir = subprocess.getstatusoutput("%s shell ''mkdir %s''" % (self.commod, filePath))
        status, message = mkdir[0], mkdir[1]
        if status == 0 or "Success" in message:
            logger.info("创建文件夹%s成功" % (tail))
        elif "File exists" in message:
            logger.error("文件夹已存在跳过创建！！！")
        else:
            logger.error("文件夹创建失败 ErrorInfo：%s" % (message))

    def removeFile(self,filePath):
        """
        删除文件
        :return:
        """
        # remove = subprocess.getstatusoutput('%s shell "rm -rf %s" ' % (self.commod, filePath))
        # 判断文件夹是否存在来检测是否被删除成功（暂未找到更好的办法处理判断）
        path = subprocess.getstatusoutput('%s shell "cd %s" ' % (self.commod, filePath))
        status,message = path[0],path[1]
        if "No such file or directory" in message:
            logger.info("设备：%s 已成功删除掉文件： %s"%(self.devicesId,filePath))
        else:
            logger.info("设备：%s 删除文件失败"%(self.devicesId))

    def pullFile(self,filePath,targetPath):
        """
        将Phone设备中的运行日志Pull至PC
        :param filePath:
        :param targetPath:
        :return:
        """

        pullInfo =subprocess.getoutput("%s pull %s %s"%(self.commod,filePath,targetPath))
        if "adb: error" in pullInfo:
            logger.info("Pull文件至移动端：%s失败，ErrorInfo：%s"%(self.devicesId,pullInfo))
        else:
            logger.info("Pull File is Ok")

    def pushFile(self,filePath,targetPath):
        """
        Push文件至移动端
        :param filePath:
        :param targetPath:
        :return:
        """
        pushInfo =subprocess.getoutput("%s push %s %s"%(self.commod,filePath,targetPath))
        if "adb: error" in pushInfo:
            logger.info("Push文件至移动端：%s失败，ErrorInfo：%s"%(self.devicesId,pushInfo))
        else:
            logger.info("Push File is Ok")

    def getProcess(self, packages):
        """
        获取进程信息
        :param packages: 包名
        :return:
        """
        process = subprocess.getstatusoutput("%s shell ps |grep '%s'" % (self.commod, packages))
        status,messages = process[0],process[1]
        if status == 0:
            logger.info("\n%s" % (messages))
            return process
        else:
            logger.error("暂未获取到%s的进程信息" % (packages))
            return False

    def getScreenshot(self,target):
        """
        手机截图
        :param nowtime 当前本地格式化的毫秒级时间
        :param target: 目标路径
        :param screen_info 返回的信息，格式：['1','Error opening file: path (Read-only file system)']
        :param screen_status 截图时的状态
        :return:
        """
        nowtime = datetime.datetime.now().strftime('%Y-%m%d-%H-%M-%S-%f')
        logger.info(nowtime)
        filePath = "/%s/%s.png" % (target, nowtime)
        screen = subprocess.getstatusoutput("adb -s %s shell screencap -p %s" % (self.devicesId, filePath))
        screen_status = screen[0]
        if screen_status == 0:
            logger.info("截图成功%s" % (filePath))
            return filePath
        else:
            logger.error("%s" % (screen[1]))
            return False

    def analysisCrash(self, filePath):
        """
        分析logcat日志
        :param key_word：关键字
        :param filePath：文件路径
        :return: count   用于统计数量
       """
        try:
            if os.path.exists(filePath):
                logger.info("正在过滤文本：%s"%(filePath))
                with open(filePath,"r") as file:
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
                    logger.info("Bug数量：%s   行数：%s"%(count,rows))
        except FileNotFoundError:
            logger.error('无法打开指定的文件！！！')
        except LookupError:
            logger.error('指定了未知的编码！！！')
        except UnicodeDecodeError:
            logger.error('读取文件时解码错误！！！')

    def getPhoneInfo(self):
        """
        得到手机信息(ROOT手机(处理起来不是很好且市面上root手机覆盖率较小、先放着后期搞)、非ROOT手机不同处理)
        :param release:系统版本
        :param model:型号
        :param brand：品牌
        :param device_id 设备号
        :return: result 以上综合信息
        """
        release = subprocess.getstatusoutput("%s shell getprop ro.build.version.release" % (self.commod))[1].strip()
        model = subprocess.getstatusoutput("%s shell getprop ro.product.model" % (self.commod))[1].strip()
        vm_size = subprocess.getstatusoutput("%s shell wm size" % (self.commod))[1]
        result = {"release": release, "model": model, "vm_size": vm_size}
        logger.info(result)
        return release, model, vm_size

    def getDeviceTime(self):
        """
        获取设备时间
        :return:
        """
        time = subprocess.getstatusoutput("adb -s %s shell date" % (self.commod))[1]
        logger.info("当前系统时间：%s" % (time))
        return time

    def getMenTotal(self):
        """
        得到内存 (ROOT用户使用)
        :param devices:设备号
        :return: men_total
        """
        cmd = '%s shell cat /proc/meminfo' % (self.commod)
        get_cmd = os.popen(cmd).readlines()
        men_total = 0
        men_total_str = "MemTotal"
        for line in get_cmd:
            if line.find(men_total_str) >= 0:
                men_total = line[len(men_total_str) + 1:].replace("kB", "").strip()
                break
        logger.info("得到设备：%s的内存：%s" % (self.devicesId, str(men_total) + "-KB"))
        return str(men_total) + "-KB"


    def getCpuKel(self):
        """
        得到CPU内核版本 (ROOT用户使用)
        :param devices:
        :return: int_cpu
        """
        cmd = " %s shell cat /proc/cpuinfo"%(self.commod)
        get_cmd = os.popen(cmd).readlines()
        find_str = "processor"
        int_cpu = 0
        for line in get_cmd:
            if line.find(find_str) >= 0:
                int_cpu += 1
                logger.info("得到设备：%s的CPU内核版本：%s" % (self.devicesId, str(int_cpu) + "核"))
                return str(int_cpu) + "核"

    def fileExists(self, target):
        """
        判断文件在目标路径是否存在
        :param devices:设备号
        :param target：目标文件路径
        :return: True
        """
        file = subprocess.getstatusoutput("%s shell ls %s" % (self.commod, target))
        if file[0] == 1:
            logger.error("%s文件不存在！！！" % (target))
            return False
        else:
            logger.info("%s文件存在！！！" % (target))
            return True

    def isInstall(self, package):
        """
        判断目标app在设备上是否已安装
        :param package: 目标app包名
        :return:
        """
        file = subprocess.getstatusoutput("%s shell pm list packages %s" % (self.commod, package))
        logger.info("grepPackage："%(file))
        if file[1] == "":
            logger.error("本地未安装：%s" % (package))
            return False
        else:
            logger.info("本地已安装：%s" % (package))
            return package

    def getDisplayState(self):
        """
        获取屏幕状态(部分手机特别是华为、该方法不可用、后续再摸索)
        :return: window_policy 亮屏(mScreenOnEarly=true mScreenOnFully=true )/灭屏(mScreenOnEarly=False mScreenOnFully=False )
        """
        window_policy = \
        subprocess.getstatusoutput("%s shell dumpsys window policy|grep mScreenOn" % (self.commod))[1].strip()
        logger.info("当前屏幕状态：%s " % (window_policy))
        return window_policy

    def rotation_screen(self, param):
        """
        旋转屏幕
        :param param: 0 >> 纵向，禁止自动旋转; 1 >> 自动旋转
        :return:
        """
        subprocess.getstatusoutput('%s shell /system/bin/content insert --uri content://settings/system --bind '
                   'name:s:accelerometer_rotation --bind value:i:%s'%(param))

    def getPsPid(self,package):
        """
        获取进程pid
        :param package: 包名
        :return: pid
        """
        ps_pid = subprocess.getstatusoutput("%s shell ps |grep '%s' " % (self.commod, package))
        pid_split = ps_pid[1].strip().split(" ")
        while "" in pid_split:
            pid_split.remove("")
        pid = pid_split[1]
        if ps_pid[0] == 0:
            logger.info("%s成功获取到：%s - Pid：%s " % (self.devicesId, package, pid))
            return pid
        else:
            logger.error("%s获取进程失败！！！" % (package))

    def killProcess(self,pid):
        """
        杀死进程 需要Root权限不推荐使用
        :return: kill_pid
        """
        kill = subprocess.getstatusoutput("%s shell kill %s " % (self.commod, pid))[1].strip()
        logger.info("%s" % (kill))
        return kill

    def startApp(self,package):
        """
        启动一个应用
        :return start_app：开启
        """
        start = subprocess.getstatusoutput("%s shell am start -n %s" % (self.commod, package))[1].strip()
        logger.info("正在启动：%s " % (package))
        return start

    def forceApp(self, package):
        """
        退出应用
        :return: quit_app
        """
        stop = subprocess.getstatusoutput("%s shell am force-stop %s " % (self.commod, package))
        logger.info("已成功退出%s " % (package))
        return stop

    def reboot(self):
        """
        重启Iphone
        :param reboot:重启
        :return: reboot_info
        """
        reboot = subprocess.getstatusoutput("%s shell reboot" % (self.commod))
        logger.info("设备ID：%s 正在重启请稍后！！！" % (self.devicesId))
        return reboot

    def recovery(self):
        """
        重启设备并进入recovery模式
        :return: recovery
        """
        recovery = subprocess.getstatusoutput("%s shell reboot recovery " % (self.commod))
        if recovery[0] == "0":
            logger.info("设备%s已成功重启设备并进入recovery模式" % (self.devicesId))
            return True
        else:
            logger.error("设备%s进入recovery模式失败"%(self.devicesId))

    def fastboot(self):
        """
        重启设备并进入fastboot模式
        :return: fastboot
        """
        fastboot = subprocess.getstatusoutput("%s shell reboot bootloader " % (self.commod))[1].strip()
        logger.info("设备%s已成功重启设备并进入fastboot模式" % (self.devicesId))
        return fastboot

    def getWifiState(self):
        """
        获取WiFi连接状态
        :return: wifi_state
        """
        state = subprocess.getstatusoutput("%s shell dumpsys wifi | grep ^Wi-Fi " % (self.commod))[1].strip()
        if state == "Wi-Fi is disabled":
            logger.error("%s " % (state))
            return False
        else:
            logger.info("%s " % (state))
            return state

    def getDataState(self):
        """
        获取移动网络连接状态
        :return: state
        """
        state = subprocess.getstatusoutput("%s shell dumpsys telephony.registry | grep 'mDataConnectionState'" % (self.commod))[1].strip()
        if "mDataConnectionState=-1" in state:
            logger.error("设备：%s 未启用移动网络 详情：%s"%(self.devicesId,state.replace("\n","")))
            return False
        else:
            return state

    def getNetworkState(self):
        """
        设备是否连上互联网
        :return:True
        """
        network = subprocess.getstatusoutput("%s shell ping -w 1 www.baidu.com" % (self.commod))[1].strip()
        if "ping: unknown host" in network:
            logger.error("网络未连接！！！")
        else:
            logger.info("设备已连上互联网：%s " % (network))
            return True

    def getWifiPassword(self):
        """
        获取WIFI密码列表
        :return:
        """
        if not self.root():
            print('The device not root.')
            return []
        l = re.findall(re.compile('ssid=".+?"\s{3}psk=".+?"'), subprocess.getstatusoutput('%s shell su -c cat /data/misc/wifi/*.conf'%(self.commod))[1])
        return [re.findall(re.compile('".+?"'), i) for i in l]

    def call(self, number):
        """
        拨打电话
        :param index：设备序列
        :param number: 电话号码
        :return:call_info
        """

        call_info = subprocess.getstatusoutput("%s shell am start -a android.intent.action.CALL -d tel:%s" % (self.commod, number))[1].strip()
        logger.info("正在呼叫：%s " % (call_info))
        return call_info

    def openUrl(self,devices,url):
        """
        打开网页
        :return: openUrl
        """

        openUrl = subprocess.getstatusoutput("%s shell am start -a android.intent.action.VIEW -d %s" % (self.commod, url))[1].strip()
        logger.info("%s " % (openUrl))
        return openUrl

    def sendKey(self, keyword):
        """
        发送一个按键事件即键盘输入
        :param keyword：按键按键事件
        :return: send_key
        """
        send_key = subprocess.getstatusoutput("%s shell input keyevent %s" % (self.commod, keyword))[1].strip()
        logger.info("正在疯狂输入：%s " % (keyword))
        return send_key

    def switchDir(self,filePath=""):
        """
        切换目录(写到一半不想写的def 也不怎么常用到先别引用、先占个位)
        :return: dir_path
        """
        switch = subprocess.getstatusoutput("%s shell cd %s" % (self.commod, filePath))
        logger.info(switch)

if __name__ == '__main__':
    adb = AdbManage()
    # adb.getRootStatus()
    # adb.checklocal("com.mryu.devstudy")
    # adb.installApk(r"D:\Work_Spaces\PyCharm_Project\AutoFramework\ApkPath\app-release.apk")
    # adb.clearPackage("com.mryu.devstudy")
    # adb.getIpconfig()
    # adb.remoteConnectdev("10.94.253.120")
    # adb.grepActivity()
    # adb.getBatteryInfo()
    # adb.createFile("mkdir","/sdcard/AutoMonkey")
    # adb.removeFile("/sdcard/AutoMonkey")
    # adb.pullFile("/sdcard/AutoMonkey",r"D:\Work_Spaces\PyCharm_Project\AutoFramework\Result")
    # adb.pushFile(r"D:\Work_Spaces\PyCharm_Project\AutoFramework\Result","/sdcard")
    # adb.getProcess("com.tencent.mobileqq")
    # adb.getScreenshot("/sdcard")
    # adb.getPhoneInfo()
    # adb.getDeviceTime()
    # adb.getMenTotal()
    # adb.getCpuKel()
    # adb.isInstall("com.mryu.devstudy")
    # adb.getDisplayState()
    # adb.getPsPid("com.mryu.devstudy")
    # adb.killProcess(15621)
    # adb.forceApp("com.mryu.devstudy")
    # adb.getWifiState()
    # adb.getDataState()
    # adb.getNetworkState()
    # adb.getMacAddress()
    # adb.call(15666)
    # adb.reboot()
    # adb.recovery()
    # adb.fastboot()
    # adb.analysisCrash(r"E:\WorkSpace\PycharmProjects\AutoFramework\Result\AutoMonkey\20200109-Crash.log")
    # adb.grepEnterActivity("com.mryu.devstudy")