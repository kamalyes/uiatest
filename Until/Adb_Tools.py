#!/usr/bin/env python 3.7
# -*- coding:utf-8 -*-
'''
# FileName： Adb_Tools.py
# Author : v_yanqyu
# Desc: PyCharm
# Date： 2020/9/6 18:41
'''
__author__ = 'v_yanqyu'
import os,re,time,datetime
import configparser,subprocess
from Logger import GlobalLog
from ATestClass import ImportJar
from Until import GetAbspath

logger = GlobalLog.Logger.write_log()
ImportJar.check_import()
conf_ini = "../Config/Logger.ini"
conf = configparser.ConfigParser()
conf.read(conf_ini)
package_name = conf.get("Apk_Info", "package_name")

def check_local_file():
    """
    检查本地文件是否存在
    :param superiordirectory:上级目录
    :param GeneralFile:拼接后的APK包存储目录
    :return apk_filepath：拼接后的安卓包完整目录
    """
    apklist = []
    superiordirectory = GetAbspath.get_superiordirectory()
    logger.info("上级所在目录为：{}" .format(superiordirectory))
    GeneralFile =superiordirectory + "\APKPath"
    logger.info("APK存储路径：{}" .format(GeneralFile))
    try:
        for File_Path in os.listdir(GeneralFile):
            apklist.append(File_Path)
            logger.info("检索到APK_Name：{}".format(File_Path))
            apk_filepath = GeneralFile + "\\" + File_Path
            return apk_filepath
    except Exception as TypeError:
        logger.error(TypeError)

def check_adb_path():
    """
    检查adb 判断是否设置环境变量ANDROID_HOME
    :return:
    """
    adb_info = os.popen("adb version").read()# window下使用findstr
    error_message = "'adb'不是内部或外部命令，也不是可运行的程序或批处理文件。"
    if adb_info in error_message:
        return False
    else:
        return True

def check_devices_status():
    """
    检查设备是否连接成功，如果成功返回Device_Nmae，否则返回False
    :param all_info：CMD输入
    :return devices_name：设备ID
    """
    try:
        adb_info = check_adb_path()
        if adb_info == True:
            logger.info("----------Start Connect Device--------------")
            str_init = ' '
            all_info = os.popen('adb devices').readlines()
            for i in range(len(all_info)):
                str_init += all_info[i]
            devices_name = re.findall('\n(.+?)\t', str_init, re.S)
            if devices_name !=[]:
                logger.info("设备连接成功%s"%(devices_name))
                return devices_name
            else:
                logger.error("请检查目标设备是否与主机连接成功！！！")
                return False
        else:
            logger.error("本地没有配置Android_SDK环境！！！")
    except Exception as TypeError:
        logger.error("Device Connect Fail:",TypeError)

def install_apk(apk_filepath,devices_name):
    """
    检查本地文件是否存在
    :param devices_name:设备号
    :param apk_filepath：拼接后的安卓包完整目录
    """
    try:
        logger.info("成功接收到check_local_file方法return的安装包绝对路径：{}".format(apk_filepath))
        logger.info("----------Start Install APK--------------")
        if devices_name == False:
            pass
        else:
            # 循环遍历出所有已连接的终端设备,便于后期调用
            logger.info('检索到的设备：{}'.format(devices_name))
            for dev_name in  devices_name:
                logger.info("当前被安装终端ID：%s，安装过程中请勿移除USB连接！！！"%(dev_name))
                result = os.popen('adb -s %s install -r %s' % (dev_name, apk_filepath))
                res = result.read()
                for line in res.splitlines():
                    if line == "Success":
                        logger.info("设备：%s安装成功"%(dev_name))
                    else:
                        logger.error("设备：%s安装失败！！！" % (dev_name))
    except Exception as ModuleNotFoundError:
        logger.error(ModuleNotFoundError)

def uninstall_apk(devices_name):
    """
    卸载apk
    :param devices_name:设备号
    :param package_name:包名
    """
    try:
        if devices_name == False:
            pass
        else:
            logger.info("------- Uninstall Apking ------")
            for dev_name in  devices_name:
                logger.info("当前被安装终端ID：%s，卸载过程中请勿移除USB连接！！！"%(dev_name))
                result = os.popen('adb -s %s uninstall  %s' % (dev_name, package_name))
                res = result.read()
                for line in res.splitlines():
                    if line == "Success":
                        logger.info("设备：%s卸载成功"%(dev_name))
                    else:
                        logger.error("设备：%s卸载失败！！！" % (dev_name))
    except Exception as ModuleNotFoundError:
        logger.error(ModuleNotFoundError)

def clear_package(devices_name):
    """
    清理apk缓存
    :param devices_name:设备号
    :param package_name:包名
    """
    try:
        if devices_name ==False:
            pass
        else:
            logger.info("------- Clear Package ------")
            for dev_name in  devices_name:
                logger.info("当前被安装终端ID：%s，卸载过程中请勿移除USB连接！！！"%(dev_name))
                result = os.popen('adb shell pm clear  %s' % (package_name))
                res = result.read()
                for line in res.splitlines():
                    if line == "Success":
                        logger.info("设备：%s清除数据成功" % (dev_name))
                    elif line == "Failed":
                        logger.error("设备：%s清除数据失败！！！" % (dev_name))
                    else:
                        logger.error("未知错误")
    except Exception as ModuleNotFoundError:
        logger.error(ModuleNotFoundError)

def get_ipconfig(devices_name):
    """
    获取已连接的手机IP
    :param ipconfig：wlan0基本Ip信息
    :return ip
    """
    try:
        for dev_name in devices_name:
            if devices_name == False:
                logger.error("adb.exe: more than one device/emulator")
            else:
                ipconfig = os.popen("adb shell ifconfig wlan0").read()  # window下使用findstr
                ip = ipconfig[31:45].replace("B","")
                logger.info("检索到设备%s当前IP：%s"%(dev_name,ip))
                return  ip
    except Exception as ModuleNotFoundError:
        logger.error(ModuleNotFoundError)

def remote_connectdev(ip):
    """
    远程连接手机
    :param check_ip：检查网络是否通
    :return devices_name：设备ID
    """
    check_ip = os.popen("ping {}".format(ip)).read()
    restart_adb = os.popen("adb tcpip 5555").read()
    str = "Ping 请求找不到主机 None。请检查该名称，然后重试。"
    if str == check_ip or restart_adb == "":
        logger.error("adb tcpip模式重启adb失败%s"%(check_ip))
    else:
        logger.info("adb tcpip模式重启adb成功！！！")
        connect = os.popen("adb connect {}".format(ip)).read()
        logger.info(connect)
    return check_ip

def get_current_package(devices_name):
    '''
    获取当前运行
    :param devices_name: 设备号
    :return: pwd_activity：package/activity
    '''
    try:
        for dev_name in devices_name:
            activity = os.popen("adb shell dumpsys window windows | grep -E 'mCurrentFocus'").read() # window下使用findstr
            pwd_activity =activity.replace(" ","")
            logger.info("检索到设备%s当前Activity：%s"%(dev_name,pwd_activity))
            return  pwd_activity
    except Exception as ModuleNotFoundError:
        logger.error(ModuleNotFoundError)

def get_battery_info(devices_name):
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
    try:
        for dev_name in devices_name:
            battery = os.popen("adb shell dumpsys battery").read().split("\n") # window下使用findstr
            batterystatus = battery[7]
            batterylevel  = battery[10]
            logger.info("成功获取到{}设备电池信息：{},{}".format(dev_name,batterystatus,batterylevel))
            return battery,batterystatus,batterylevel
    except Exception as  ModuleNotFoundError:
        logger.error(ModuleNotFoundError)

def create_file(devices_name,model,path=""):
    """
    创建目录
    :param  split_path：清理文件尾椎
    :param  mkdir_msg：运行后返回的结果集 1代表False、0代表True
    :param  model: 调用的方法元素、mkdir：创建文件、 touch：创建文件夹
    :param  make_dir：创建文件夹、且会携带返回结果集
    :param  touch_file: 创建文件
    :param  devices_name：设备号
    """
    try:
        if devices_name == False:
            pass
        else:
            if model == "mkdir":
                # 清理文件尾椎例如：/sdcard/maketest/aaa.text 自动过滤掉为/sdcard/maketest/aaa
                split_path = os.path.splitext(path)[0]
                logger.info("------- Make Directory------")
                make_dir = subprocess.getstatusoutput('adb shell "mkdir %s"'%(split_path))
                if make_dir[0] == 1:
                    logger.error("%s"%(make_dir[1]))
                else:
                    logger.info("%s Mkdir 成功"%(make_dir))
                    return split_path

            elif model == "touch":
                logger.info("------- Touch File------")
                for dev_name in devices_name:
                    touch_file = subprocess.getstatusoutput('adb shell "touch %s"' %(path))
                    if touch_file[0] == 1:
                        logger.info("%s" % (touch_file[1]))
                    elif touch_file[0] == 0:
                        logger.error("%s Touch 成功" % (path))
                        return touch_file
                    else:
                        logger.error("未知错误")
                else:
                    pass
    except Exception as ModuleNotFoundError:
        logger.error(ModuleNotFoundError)


def file_transfer(devices_name,model,source,target=""):
    """
    文件基本操作
    :param pull 从手机端拉取文件到电脑端
    :param push 从电脑端复制文件至手机端
    :param remove：强制删除文件
    :param subprocess方法检查返回结果集 1为假 0为真 反人类
    """
    try:
        if devices_name == False:
            pass
        else:
            if model == "pull" or model == "Pull":
                pull = subprocess.getstatusoutput('adb pull %s %s"' % (source, target))
                logger.debug(pull)
                if pull[0] == 0:
                    logger.info("Pull：%s文件到 %s成功." % (source, target))
                    return pull
                else:
                    logger.error("Pull文件失败，%s" % (pull[1].replace(": ","_")))

            elif model == "push" or model == "Push":
                push = subprocess.getstatusoutput('adb push %s %s"' % (source, target))
                if push[0] == 0:
                    logger.info("Push：%s文件到 %s" % (source, target))
                    return push
                else:
                    logger.error("Push文件失败，%s" % (push[1].replace(": ", "_")))

            elif model == "remove" or model == "Remove":
                remove = subprocess.getstatusoutput('adb shell "rm -rf %s" ' % (source))
                if remove[0]:
                    logger.info("删除%s文件成功" % (source))
                    return remove
                else:
                    logger.error("删除文件失败！！！")
            else:
                logger.error("未知错误！！！")
    except Exception as TypeError:
        logger.error(TypeError)

def get_process(devices_name):
    """
    获取进程信息
    :param devices_name: 设备ID
    :param process: 进程info
    :return: process_id
    """
    try:
        if devices_name == False:
            pass
        else:
            process =subprocess.getstatusoutput("adb shell 'ps |grep keyword'")
            logger.info(process)
    except Exception as TypeError:
        logger.error(TypeError)

def get_screenshot(devices_name,source):
    """
    手机截图
    :param nowtime 当前本地格式化的毫秒级时间
    :param target: 目标路径
    :param screen_info 返回的信息，格式：['1','Error opening file: path (Read-only file system)']
    :param screen_status 截图时的状态
    :return:
    """
    try:
        nowtime = datetime.datetime.now().strftime('%Y-%m%d-%H-%M-%S-%f')
        logger.info(nowtime)
        path ="/%s/%s.png"%(source,nowtime)
        screen_info = subprocess.getstatusoutput("adb shell screencap -p %s"%(path))
        screen_status = screen_info[0]
        if screen_status == 0:
            logger.info("截图成功%s"%(path))
            return path
        else:
            logger.error("%s"%(screen_info[1]))
            return False
    except Exception as TypeError:
        logger.error(TypeError)

def get_cache_logcat():
    """
    导出缓存日志
    :return:
    """

def get_crash_logcat(self):
    """
    导出崩溃日志
    :return:
    """
    return self.adb('logcat -v time -d | %s AndroidRuntime' % (self.__find,))

def clear_cache_logcat(self):
    """
    清理缓存区日志
    :return:
    """
    self.adb('logcat -c')

def get_device_time(self):
    """
    获取设备时间
    :return:
    """
    return self.shell('date').read().strip()



if __name__ == '__main__':
    # check_devices_status()
    # install_apk(check_local_file(),check_devices_status())
    # clear_package(check_devices_status())
    # get_current_package(check_devices_status())
    # get_battery_info(check_devices_status())
    # remote_connectdev(get_ipconfig(check_devices_status()))
    # create_file(check_devices_status(),model="touch",path="/sdcard/mkdirtes/test.txt")
    # get_current_package(check_devices_status())
    # file_transfer(check_devices_status(),model="remove",source="/sdcard/mkdirtes")
    # get_process(check_devices_status())
    get_screenshot(check_devices_status(),source="sdcard")