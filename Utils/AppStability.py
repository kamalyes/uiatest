# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： AppStability.py
# Author : v_yanqyu
# Desc: Monkey脚本
# Date： 2020/10/23 10:57
'''
import re,os,sys,time
import subprocess
from Logger.GlobalLog import Logger
from Utils.ConfigParser import  IniHandle
from Utils.DirTools import  Doc_Process
from Utils.AdbTools import Adb_Manage
IniHandle = IniHandle()
Adb = Adb_Manage()
logger = Logger.write_log()
getpwd =Doc_Process.get_superior_dir()
class Monkey():
    def __init__(self,method=None):
        """
        初始全局运行method/commod
        :param method 运行方式 默认存储sdcard 加特殊条件则存储至local
        :param commod  命令
        """
        # 文件读取及存储的路径
        self.package = IniHandle.optvalue(node="Monkey_Test",key="package")
        self.local = IniHandle.optvalue(node="Monkey_Test",key="local")
        self.sdcard = IniHandle.optvalue(node="Monkey_Test",key="sdcard")
        self.whiteapath = IniHandle.optvalue(node="Monkey_Test",key="whiteapath")

        self.apkpath =os.path.join(getpwd,IniHandle.optvalue(node="Monkey_Test",key="apkpath"))
        self.local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if method == "local":
            self.crashlog = os.path.join(getpwd,self.local,"Crashlog.log")
            self.monkeylog = os.path.join(getpwd,self.local,"RunMonkey.log")
            self.mangerlog = os.path.join(getpwd,self.local,"ActivtyMansger.log")
        else:
            # self.mkdir = "%s/%s"%(self.sdcard, self.local_date)
            # subprocess.getstatusoutput('adb shell mkdir -p %s'%(self.mkdir))
            self.crashlog = os.path.join('%s/Crash.log'%(self.sdcard))
            self.monkeylog = os.path.join("%s/RunMonkey.log"%(self.sdcard))
            self.mangerlog = os.path.join("%s/ActivtyMansger.log"%(self.sdcard))

        # commod 命令
        self.operation = IniHandle.optvalue(node="Monkey_Test",key="operation")
        self.ignore =  IniHandle.optvalue(node="Monkey_Test",key="ignore")
        self.commod = ('%s %s'%(self.operation,self.ignore))
        # MAinActivity&白名单窗口
        self.mainactivity = IniHandle.optvalue(node="Monkey_Test",key="mainactivity")
        self.devices = IniHandle.optvalue(node="Monkey_Test", key="devices").split(";")

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

    def backwhite(self):
        """
        通过白名单机制进行二次封装Monkey自定义Activity
        :return:
        """
        whitelist =[]
        content = os.popen('adb shell dumpsys activity  |findstr "mResumedActivity" ').read()  # 读取当前页面
        activity = re.compile(r'com.*').findall(content)[0].split(' ')[0]
        for line in open(self.whiteapath):
            whitelist.append(line.strip())
        if activity not in whitelist:
            logger.info('当前运行窗口：%s'%(activity))
            start = subprocess.getstatusoutput('adb shell am start -n %s/%s' % (self.package, self.mainactivity))
            logger.info("成功返回主窗口：%s" % (start[1]))
        else:
            logger.info("当前位于：%s不需要跳转！！！" % (activity))

    @classmethod
    def statusbar(self,method,devices):
        """
        开启/关闭状态栏
        :param method: 方式：开启还是关闭
        :param devices: 设备号
        :return:
        """
        if method == 'open':
            os.popen('adb -s %s shell settings put global policy_control null' % (devices))
            os.popen('adb -s %s shell wm overscan 0,0,0,0' % (devices))
            logger.info("已恢复状态栏&底下的返回控件")

        elif method == 'close':
            os.popen('adb -s %s shell settings put global policy_control immersive.full=*' % (devices))
            os.popen('adb -s %s shell wm overscan 0,0,0,-200' % (devices))
            logger.info("运行前关闭一些障碍 隐藏掉状态栏&底下的返回控件")


    def native(self):
        """
        运行前环境部署/原生态的Monkey瞎跑
        :return:
        """
        devices = Adb.check_devices_status()
        if devices !=False:
            for i in range(len(devices)):
                if devices[i] in self.devices or devices is not None:
                    packages = self.checklocal()
                    logger.info('接收到checklocal方法传回来的包名信息：%s%s' % (packages, type(packages)))
                    if packages[i] == '':
                        logger.warning("当前设备：%s 没有安装被测软件即将安装：%s" % (devices[i], self.apkpath))
                        status = subprocess.getstatusoutput('adb -s %s install -r %s' % (devices[i], self.apkpath))
                        if 'Success' in status[1]:
                            logger.info("设备%s：安装%s成功" % (devices[i], self.apkpath))
                        elif 'No such file or directory' in status[1]:
                            logger.error("设备%s安装失败，错误信息：%s" % (devices[i], status[1]))
                        else:
                            installInfo = re.compile('INSTALL.*').findall(status[1])[0].replace(']', '')
                            errors = {
                                # 安装错误常见列表
                                'INSTALL_FAILED_ALREADY_EXISTS': '程序已经存在',
                                'INSTALL_DEVICES_NOT_FOUND': '找不到设备',
                                'INSTALL_FAILED_DEVICE_OFFLINE': '设备离线',
                                'INSTALL_FAILED_INVALID_APK': '无效的APK',
                                'INSTALL_FAILED_INVALID_URI': '无效的链接',
                                'INSTALL_FAILED_INSUFFICIENT_STORAGE': '没有足够的存储空间',
                                'INSTALL_FAILED_DUPLICATE_PACKAGE': '已存在同名程序',
                                'INSTALL_FAILED_NO_SHARED_USER': '要求的共享用户不存在',
                                'INSTALL_FAILED_UPDATE_INCOMPATIBLE': '版本不能共存',
                                'INSTALL_FAILED_SHARED_USER_INCOMPATIBLE': '需求的共享用户签名错误',
                                'INSTALL_FAILED_MISSING_SHARED_LIBRARY': '需求的共享库已丢失',
                                'INSTALL_FAILED_REPLACE_COULDNT_DELETE': '需求的共享库无效',
                                'INSTALL_FAILED_DEXOPT': 'dex优化验证失败',
                                'INSTALL_FAILED_DEVICE_NOSPACE': '手机存储空间不足导致apk拷贝失败',
                                'INSTALL_FAILED_DEVICE_COPY_FAILED': '文件拷贝失败',
                                'INSTALL_FAILED_OLDER_SDK': '系统版本过旧',
                                'INSTALL_FAILED_CONFLICTING_PROVIDER': '存在同名的内容提供者',
                                'INSTALL_FAILED_NEWER_SDK': '系统版本过新',
                                'INSTALL_FAILED_TEST_ONLY': '调用者不被允许测试的测试程序',
                                'INSTALL_FAILED_CPU_ABI_INCOMPATIBLE': '包含的本机代码不兼容',
                                'CPU_ABIINSTALL_FAILED_MISSING_FEATURE': '使用了一个无效的特性',
                                'INSTALL_FAILED_CONTAINER_ERROR': 'SD卡访问失败',
                                'INSTALL_FAILED_INVALID_INSTALL_LOCATION': '无效的安装路径',
                                'INSTALL_FAILED_MEDIA_UNAVAILABLE': 'SD卡不存在',
                                'INSTALL_FAILED_INTERNAL_ERROR': '系统问题导致安装失败',
                                'INSTALL_PARSE_FAILED_NO_CERTIFICATES': '禁止了USB模式下安装应用文件未通过认证 >> 设置开启未知来源',
                                'INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES': '文件认证不一致 >> 先卸载原来的再安装',
                                'INSTALL_FAILED_INVALID_ZIP_FILE': '非法的zip文件 >> 先卸载原来的再安装',
                                'INSTALL_CANCELED_BY_USER': '需要用户确认才可进行安装',
                                'INSTALL_FAILED_VERIFICATION_FAILURE': '验证失败 >> 尝试重启手机',
                                'INSTALL_FAILED_CANCELLED_BY_USER': '验证授权失败,用户主动取消安装',
                                'DEFAULT': '未知错误',
                                'adb: failed to stat': '本地没有安装包'
                            }
                            logger.error("设备%s安装失败，错误信息：%s %s" % (devices[i], installInfo,errors[installInfo]))
                    else:
                        logger.info("当前设备 %s 已安装被测软件：%s" % (devices[i], packages[i]))
                        try:
                            Monkey.statusbar(method='close',devices=devices[i])
                            os.popen('adb -s %s shell logcat -c && adb -s %s shell logcat -b crash > %s'%(devices[i],devices[i],self.crashlog))
                            os.popen('adb -s %s shell logcat ActivityManager:I *:s > %s' % (devices[i],self.mangerlog))
                            os.popen('adb -s %s shell monkey -p %s %s >%s'%(devices[i],self.package,self.commod,self.monkeylog))
                        except Exception as e:
                            logger.error(e)
                        finally:
                            Monkey.statusbar(method='open',devices=devices[i])

if __name__ == '__main__':
    Monkey(method='local').native()
    # Monkey().backwhite()