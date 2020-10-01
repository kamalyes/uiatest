# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： AdbTools.py
# Author : v_yanqyu
# Desc: Adb工具类
# Date： 2020/9/6 18:56
'''
__author__ = 'v_yanqyu'
import os,re
import platform,datetime
import configparser,subprocess
from Logger import GlobalLog
from Utils import DirTools
logger = GlobalLog.Logger().write_log()#调用日志模块

conf_ini = r"../Config/config.ini"
conf = configparser.ConfigParser()
conf.read(conf_ini,encoding="utf-8")
package_name = conf.get("Android-Info", "package_name")

# logger.info(package_name)

class Adb_Manage(object):
    def check_filtered(self):
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

    def check_local_file(self):
        """
        检查本地文件是否存在
        :param superiordirectory:上级目录
        :param general_file:拼接后的APK包存储目录
        :return apk_filepath：拼接后的安卓包完整目录
        """
        apklist = []
        superiordirectory = DirTools.Doc_Process().get_superior_dir()
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

    def check_adb_path(self):
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

    def check_devices_status(self):
        """
        检查设备是否连接成功，如果成功返回Device_Nmae，否则返回False
        :param devices_info：CMD输入
        :return devices_name：设备ID
        """
        try:
            adb_info = self.check_adb_path()
            if adb_info == True:
                devices_name = re.findall('\n(.+?)\t', subprocess.getstatusoutput("adb devices")[1])
                if devices_name != []:
                    logger.info("设备连接成功%s" % (devices_name))
                    return devices_name
                else:
                    logger.error("请检查目标设备是否与主机连接成功！！！")
                    return False
            else:
                logger.error("本地没有配置Android_SDK环境！！！")
        except Exception as TypeError:
            logger.error("Device Connect Fail:", TypeError)

    def check_rootstatus(self,devices_name):
        """
        检查设备ROOT状态
        :param devices_name: 设备ID
        :param root_info：root检测用的
        :return:True：() Flase：(3, 'E must be run as root')
        """
        try:
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    root_info = subprocess.getstatusoutput("adb -s %s remount"%(dev_name))
                    if root_info[0] == 0 and root_info[1] =="remount succeeded" :
                        logger.info("设备ID：%sROOT授权成功，%s"%(dev_name,root_info[1]))
                        return True
                    else:
                        logger.error("设备ID：%s没有ROOT授权，%s"%(dev_name,root_info[1]))
                        return False
        except Exception as TypeError:
            logger.error(TypeError)

    def install_apk(self,apklist, devices_name,index=""):
        """
        检查本地文件是否存在
        :param devices_name:设备号
        :param apk_filepath：拼接后的安卓包完整目录
        """
        try:
            if devices_name == False :
                pass
            install_status = conf.get("Android-Info", "install_status")
            if install_status in(1,2):
                # 安装错误常见列表
                errors = {'INSTALL_FAILED_ALREADY_EXISTS': '程序已经存在',
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
                          'INSTALL_PARSE_FAILED_NO_CERTIFICATES': '文件未通过认证 >> 设置开启未知来源',
                          'INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES': '文件认证不一致 >> 先卸载原来的再安装',
                          'INSTALL_FAILED_INVALID_ZIP_FILE': '非法的zip文件 >> 先卸载原来的再安装',
                          'INSTALL_CANCELED_BY_USER': '需要用户确认才可进行安装',
                          'INSTALL_FAILED_VERIFICATION_FAILURE': '验证失败 >> 尝试重启手机',
                          'DEFAULT': '未知错误'
                          }

                # 循环遍历出所有已连接的终端设备,便于后期调用
                print(apklist)
                logger.info("成功接收到check_local_file方法return的安装包绝对路径：{}".format(apklist[index]))
                logger.info("检索到的设备：%s" % (devices_name))
                for dev_name in devices_name:
                    logger.info("当前终端ID：%s，安装过程中请勿移除USB连接！！！" % (dev_name))
                    install_info = subprocess.getstatusoutput(r'adb -s %s install -r %s' % (dev_name, apklist[index]))
                    install_status = install_info[1]
                    if install_status == "Success" and install_status == 1 :
                        logger.info("设备：%s安装成功！！！" % (dev_name))
                    elif install_status == "Success" and install_status == 2 :
                        logger.info("设备：%s覆盖安装成功！！！" % (dev_name))
                    else:
                        # 可在此做判断是否安装成功并展示error
                        logger.error("设备：%s安装失败%s" % (dev_name, install_info[1]))
        except Exception as TypeError:
            logger.error(TypeError)

    def uninstall_apk(self,devices_name,package_name=""):
        """
        卸载apk
        :param devices_name:设备号
        :param package_name:包名
        """
        try:
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    logger.info("当前终端ID：%s，卸载过程中请勿移除USB连接！！！" %(dev_name))
                    uninstall_info = subprocess.getstatusoutput('adb -s %s uninstall %s'%(dev_name,package_name))
                    print(uninstall_info)
                    if uninstall_info[1] == "Success":
                        logger.info("%s卸载成功%s"%(package_name,uninstall_info[1]))
                    else:
                        logger.error("%s设备卸载%s失败：%s"%(dev_name,package_name,uninstall_info[1]))
        except Exception as TypeError:
            logger.error(TypeError)

    def clear_package(self,devices_name,package_name):
        """
        清理apk缓存
        :param devices_name:设备号
        :param package_name:包名
        """
        try:
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    logger.info("当前终端ID：%s，清除数据过程中请勿移除USB连接！！！" % (dev_name))
                    clear_info = subprocess.getstatusoutput('adb -s %s shell pm clear %s'% (dev_name,package_name))
                    clear_status = clear_info[1]
                    if clear_status == "Success":
                        logger.info("设备：%s清除数据成功" % (dev_name))
                    elif clear_status == "Failed":
                        logger.error("设备：%s清除数据失败！！！" % (dev_name))
                    else:
                        logger.error("抛出异常事件，请检查本地是否已安装 %s"%(package_name))
        except Exception as TypeError:
            logger.error(TypeError)

    def get_ipconfig(self,devices_name):
        """
        获取已连接的手机WIFI_IP
        :param ipconfig：wlan0基本Ip信息
        :return ip
        """
        try:
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    ipconfig = os.popen("adb -s %s shell ifconfig wlan0"%(dev_name)).read().replace(" ","")  # window下使用findstr
                    if "wlan0:Cannotassignrequestedaddress" in ipconfig:
                        logger.error("获取%s设备WIFI_IP失败,请检查是否连接网络！！！%s" % (dev_name,ipconfig))
                    else:
                        ipv4 = re.sub("[A-Za-z]", "", str(ipconfig[31:45]))
                        logger.info("检索到设备%s当前IP：%s" % (dev_name, ipv4))
                return ipv4
        except Exception as TypeError:
            logger.error(TypeError)

    def remote_connectdev(self,devices_name, ipv4):
        """
        远程连接手机
        :param check_ip：检查网络是否通
        :return devices_name：设备ID
        """
        try:
            if ipv4 == False:
                pass
            else:
                for dev_name in devices_name:
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
        except Exception as TypeError:
            logger.error(TypeError)

    def get_current_package(self,devices_name):
        '''
        获取当前运行
        :param devices_name: 设备号
        :return: pwd_activity：package/activity
        '''
        try:
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    activity = os.popen("adb -s %s shell dumpsys window windows | grep -E 'mCurrentFocus'"%(dev_name)).read()  # window下使用findstr
                    pwd_activity = activity.strip()
                    logger.info("检索到设备%s当前Activity：%s" % (dev_name, pwd_activity))
                return pwd_activity
        except Exception as TypeError:
            logger.error(TypeError)

    def get_battery_info(self,devices_name):
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
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    battery = os.popen("adb -s %s shell dumpsys battery"%(dev_name)).read().split("\n")  # window下使用findstr
                    batterystatus = battery[7]
                    batterylevel = battery[10]
                    logger.info("成功获取到{}设备电池信息：{},{}".format(dev_name, batterystatus, batterylevel))
                return battery, batterystatus, batterylevel
        except Exception as  TypeError:
            logger.error(TypeError)

    def create_file(self,devices_name, method, filePath=""):
        """
        创建目录
        :param  split_path：清理文件尾椎
        :param  mkdir_msg：运行后返回的结果集 1代表False、0代表True
        :param  method: 调用的方法元素、mkdir：创建文件、 touch：创建文件夹
        :param  make_dir：创建文件夹、且会携带返回结果集
        :param  touch_file: 创建文件
        :param  devices_name：设备号
        """
        try:
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    if method == "mkdir":
                        # 清理文件尾椎例如：/sdcard/maketest/aaa.text 自动过滤掉为/sdcard/maketest/aaa
                        split_path = os.path.splitext(filePath)[0]
                        make_dir = subprocess.getstatusoutput('adb -s %s shell "mkdir -p %s"'% (dev_name,split_path))
                        if make_dir[0] == 1:
                            logger.error("%s Mkdir失败：%s" % (dev_name,make_dir[1]))
                        else:
                            logger.info("%s Mkdir %s成功！！！" % (dev_name,make_dir))
                            return split_path

                    elif method == "touch":
                        for dev_name in devices_name:
                            touch_file = subprocess.getstatusoutput('adb -s %s shell  "touch %s"' %(dev_name,filePath))
                            if touch_file[0] == 1:
                                logger.error("%s TouchFile失败：%s" % (dev_name,touch_file[1]))
                            elif touch_file[0] == 0:
                                logger.info("%s Touch %s 成功！！！" % (dev_name,filePath))
                                return touch_file
                            else:
                                logger.error("未知错误")
                        else:
                            pass
        except Exception as TypeError:
            logger.error(TypeError)

    def file_transfer(self,devices_name, method, source, target=""):
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
                for dev_name in devices_name:
                    if method == "pull" or method == "Pull":
                        pull = subprocess.getstatusoutput('adb -s %s pull %s %s"' % (dev_name,source, target))
                        logger.debug(pull)
                        if pull[0] == 0:
                            logger.info("%s Pull：%s文件到 %s成功." % (dev_name,source, target))
                            return pull
                        else:
                            logger.error("%s Pull文件失败，%s" % (dev_name,pull[1].replace(": ", "_")))

                    elif method == "push" or method == "Push":
                        push = subprocess.getstatusoutput('adb -s %s push %s %s"' % (dev_name,source, target))
                        if push[0] == 0:
                            logger.info("%s Push：%s文件到 %s" % (dev_name,source, target))
                            return push
                        else:
                            logger.error("%s Push文件失败，%s" % (dev_name,push[1].replace(": ", "_")))

                    elif method == "remove" or method == "Remove":
                        remove = subprocess.getstatusoutput('adb -s %s shell "rm -rf %s" ' % (dev_name,source))
                        # 以下暂未找到更好的办法处理判断是否已删除
                        if remove[0] == 0:
                            logger.info("%s删除%s文件成功" % (dev_name,source))
                            return remove
                        else:
                            logger.info("%s删除%s文件失败" % (dev_name,source))
                    else:
                        logger.error("未知错误！！！")
        except Exception as TypeError:
            logger.error(TypeError)

    def get_process(self,devices_name, keyword):
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
                for dev_name in devices_name:
                    process = subprocess.getstatusoutput("adb -s shell ps |grep '%s'" % (dev_name,keyword))
                    process_status = process[0]
                    process_info = process[1]
                    if process_status == 0:
                        logger.info("\n%s" % (process_info))
                        return process
                    else:
                        logger.error("暂未获取到%s的进程信息" % (keyword))
                        return False
        except Exception as TypeError:
            logger.error(TypeError)

    def get_screenshot(self,devices_name, source):
        """
        手机截图
        :param nowtime 当前本地格式化的毫秒级时间
        :param target: 目标路径
        :param screen_info 返回的信息，格式：['1','Error opening file: path (Read-only file system)']
        :param screen_status 截图时的状态
        :return:
        """
        try:
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    nowtime = datetime.datetime.now().strftime('%Y-%m%d-%H-%M-%S-%f')
                    logger.info(nowtime)
                    filePath = "/%s/%s.png" % (source, nowtime)
                    screen_info = subprocess.getstatusoutput("adb -s %s shell screencap -p %s" % (dev_name,filePath))
                    screen_status = screen_info[0]
                    if screen_status == 0:
                        logger.info("截图成功%s" % (filePath))
                        return filePath
                    else:
                        logger.error("%s" % (screen_info[1]))
                        return False
        except Exception as TypeError:
            logger.error(TypeError)

    def logcat_magement(self,devices_name,method,filePath):
        """
        日志管理
        :param clear_logcat  清理日志
        :param cache_logcat  缓存日志
        :param crash_logcat  crash崩溃日志
        :param history_logcat 历史crash日志（不需要二次触发）
        :return: True False
        /dev/log/main ： 主应用程序log，除了下三个外，其他用户空间log将写入此节点，包括System.out.print及System.erro.print等
        /dev/log/events ： 系统事件信息，二进制log信息将写入此节点，需要程序解析
        /dev/log/radio ： 射频通话相关信息，tag 为"HTC_RIL" "RILJ" "RILC" "RILD" "RIL" "AT" "GSM" "STK"的log信息将写入此节点
        /dev/log/system ： 低等级系统信息和debugging,为了防止mian缓存区溢出,而从中分离出来
        """
        try:
            if devices_name == False:
                pass
            else:
                for  dev_name in devices_name:
                    nowtime = datetime.datetime.now().strftime('%Y-%m%d-%H-%M-%S-%f')
                    if not os.path.exists(filePath):
                        os.makedirs(filePath)
                    if method == "logcat -c":
                        clear_logcat = subprocess.getstatusoutput("adb -s %s shell logcat -c -b main -b events -b radio -b system" % (dev_name))
                        logger.info("手机内所有日志清理完成！！！")
                    elif method == "cache_logcat":
                        cache_logcat = subprocess.getstatusoutput("adb -s %s shell logcat -c && adb logcat -v threadtime| tee %s%s.log" % (dev_name,filePath,nowtime))
                        logger.info("业务日志已重定向至%s"%(filePath))
                    elif method == "crash_logcat":
                        crash_logcat = subprocess.getstatusoutput("adb -s %s shell logcat -c && adb -s %s logcat -b crash > %s%s-Crash.log"%(dev_name,dev_name,filePath,nowtime))
                        if crash_logcat[0] == "0":
                            logger.info("日志成功保存至：%s"%(filePath))
                        else:
                            logger.error("断口或文件被占用,清理失败Error：%s"%(crash_logcat[1]))
                    else:
                        logger.error("未知错误！！！")
                    return filePath
        except Exception as TypeError:
            logger.info(TypeError)

    def analysis_crash(self, filePath,file_Name=""):
        """
        分析logcat日志
        :param key_word：关键字
        :param filePath：文件路径
        :param file_Name：文件名
        :return: count   用于统计数量
       """
        count = 0
        count_line = 0
        key_word = ['ANR', 'FATAL']
        Crash_Path =filePath+file_Name
        with open(Crash_Path, 'rt', encoding="utf-8") as f:
            for line in f:
                for word in key_word:
                    if word in line:
                        text = f.readlines()
                        with open(filePath + "/CrashInfo.txt", "a") as w:
                            w.writelines(text)
                            count += 1
                            w.close()
        f.close()
        return count

    def get_phone_info(self,devices_name):
        """
        得到手机信息(ROOT手机(处理起来不是很好且市面上root手机覆盖率较小、先放着后期搞)、非ROOT手机不同处理)
        :param release:系统版本
        :param model:型号
        :param brand：品牌
        :param device_id 设备号
        :return: result 以上综合信息
        """
        try:
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    release = subprocess.getstatusoutput("adb -s %s shell getprop ro.build.version.release" % (dev_name))[1].strip()
                    model = subprocess.getstatusoutput("adb -d -s %s shell getprop ro.product.model" % (dev_name))[1].strip()
                    vm_size = subprocess.getstatusoutput("adb -s %s shell wm size" %(dev_name))[1]
                    result = {"release": release, "model": model, "vm_size": vm_size}
                    logger.info(result)
                    # device_info = subprocess.getstatusoutput("adb devices -l")
                return release, model, vm_size

                    # print(dev_name)
                    # cmd = "adb -s " + dev_name + " shell cat /system/build.prop "
                    # # phone_info = os.popen(cmd).readlines()
                    # phone_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.readlines()
                    # release = "ro.build.version.release="  # 版本
                    # model = "ro.product.model="  # 型号
                    # brand = "ro.product.brand="  # 品牌
                    # device_id = "ro.product.device="  # 设备名
                    # result = {"release": release, "model": model, "brand": brand, "device": device_id}
                    # for line in phone_info:
                    #     for i in line.split():
                    #         temp = i.decode()
                    #         if temp.find(release) >= 0:
                    #             result["release"] = temp[len(release):]
                    #             break
                    #         if temp.find(model) >= 0:
                    #             result["model"] = temp[len(model):]
                    #             break
                    #         if temp.find(brand) >= 0:
                    #             result["brand"] = temp[len(brand):]
                    #             break
                    #         if temp.find(device_id) >= 0:
                    #             result["device"] = temp[len(device_id):]
                    #             break
                    # logger.info(result)
                    # print(dev_name)
                    # return release, model, brand, device_id
        except Exception as TypeError:
            logger.error(TypeError)


    def get_device_time(self, devices_name):
        """
        获取设备时间
        :param devices_name 设备ID
        :return: device_time 系统时间
        """
        try:
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    device_time = subprocess.getstatusoutput("adb -s %s shell date" % (dev_name))[1]
                    logger.info("当前系统时间：%s" % (device_time))
                return device_time
        except Exception as TypeError:
            logger.error(TypeError)

    def get_men_total(self,devices_name):
        """
        得到内存 (ROOT用户使用)
        :param devices_name:设备号
        :return: men_total
        """
        cmd = "adb -s " + devices_name + " shell cat /proc/meminfo"
        get_cmd = os.popen(cmd).readlines()
        men_total = 0
        men_total_str = "MemTotal"
        for line in get_cmd:
            if line.find(men_total_str) >= 0:
                men_total = line[len(men_total_str) + 1:].replace("kB", "").strip()
                break
        return int(men_total)


    def get_cpu_kel(self,devices_name):
        """
        得到CPU内核版本 (ROOT用户使用)
        :param devices_name:
        :return: int_cpu
        """
        cmd = "adb -s " + devices_name + " shell cat /proc/cpuinfo"
        get_cmd = os.popen(cmd).readlines()
        find_str = "processor"
        int_cpu = 0
        for line in get_cmd:
            if line.find(find_str) >= 0:
                int_cpu += 1
        return str(int_cpu) + "核"

    def reboot(self, devices_name):
        """
        重启Iphone
        :param reboot:重启
        :return: reboot_info
        """
        try:
           if devices_name == False:
               pass
           else:
               for index in range(len(devices_name)):
                   reboot_info = subprocess.getstatusoutput("adb -s %s shell reboot" % (devices_name[0]))
                   logger.info("设备ID：%s 正在重启请稍后！！！" % (devices_name[0]))
               return reboot_info
        except Exception as TypeError:
            logger.error(TypeError)

    def file_exists(self, devices_name, target):
        """
        判断文件在目标路径是否存在
        :param devices_name:设备号
        :param target：目标文件路径
        :return: True
        """
        try:
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    file_info = subprocess.getstatusoutput("adb -s %s shell ls %s" % (dev_name, target))
                    if file_info[0] == 1:
                        logger.error("%s文件不存在！！！" % (target))
                        return False
                    else:
                        logger.info("%s文件存在！！！" % (target))
                return True
        except Exception as TypeError:
            logger.error(TypeError)

    def is_install(self, devices_name, package_name):
        """
        判断目标app在设备上是否已安装
        :param package_name: 目标app包名
        :return:
        """
        try:
            if devices_name == False:
                pass
            else:
                for dev_name in devices_name:
                    file_info = subprocess.getstatusoutput("adb -s %s shell pm list packages %s" % (dev_name, package_name))
                    logger.info(file_info)
                    if file_info[1] == "":
                        logger.error("本地未安装：package_name：%s" % (package_name))
                        return False
                    else:
                        logger.info("本地已安装：package_name：%s" % (package_name))
                return package_name
        except Exception as TypeError:
            logger.error(TypeError)

    def get_display_state(self, devices_name,index=""):
        """
        获取屏幕状态(部分手机特别是华为、该方法不可用、后续再摸索)
        :return: window_policy 亮屏(mScreenOnEarly=true mScreenOnFully=true )/灭屏(mScreenOnEarly=False mScreenOnFully=False )
        """
        try:
            if devices_name == False:
                pass
            else:
                window_policy = subprocess.getstatusoutput("adb -s %s shell dumpsys window policy|grep mScreenOn" % (devices_name[index]))[1].replace("\n","")
                logger.info("当前屏幕状态：%s "%(window_policy))
                return window_policy
        except Exception as TypeError:
            logger.error(TypeError)

    def get_ps_pid(self,devices_name,package_name,index):
        """
        获取进程pid
        :param devices_name: 设备ID
        :param package_name: 包名
        :return: pid
        """
        try:
            if devices_name == False:
                pass
            else:
                ps_pid = subprocess.getstatusoutput("adb -s %s shell ps |grep '%s' "% (devices_name[index],package_name))
                pid_split =ps_pid[1].strip().split(" ")
                while "" in pid_split:
                    pid_split.remove("")
                pid = pid_split[1]
                if ps_pid[0] == 0:
                    logger.info("%s成功获取到：%s - Pid：%s " % (devices_name,package_name,pid))
                    return pid
                else:
                    logger.error("%s获取进程失败！！！"%(package_name))
        except Exception as TypeError:
            logger.error(TypeError)

    def kill_process(self, devices_name,index,pid):
        """
        杀死进程 需要Root权限不推荐使用
        :return: kill_pid
        """
        try:
            if devices_name == False:
                pass
            else:
                kill_pid = subprocess.getstatusoutput("adb -s %s shell kill %s " % (devices_name[index]),pid)[1].replace("\n", "")
                logger.info("进程已被干掉：%s " % (kill_pid))
                return kill_pid
        except Exception as TypeError:
            logger.error(TypeError)

    def quit_app(self, devices_name,package_name,index=""):
        """
        退出应用
        :return: quit_app
        """
        try:
            if devices_name == False:
                pass
            else:
                quit_app = subprocess.getstatusoutput("adb -s %s shell am force-stop %s " %(devices_name[index],package_name))[1].replace("\n", "")
                logger.info("已成功退出%s " % (package_name))
                return quit_app
        except Exception as TypeError:
            logger.error(TypeError)

    def recovery(self,devices_name,index):
        """
        重启设备并进入recovery模式
        :return: reboot_recovery
        """
        try:
            if devices_name == False:
                pass
            else:
                reboot_recovery = subprocess.getstatusoutput("adb -s %s reboot recovery " % (devices_name[index]))[1].replace("\n", "")
                logger.info("设备%s已成功重启设备并进入recovery模式" % (devices_name[index]))
                return reboot_recovery
        except Exception as TypeError:
            logger.error(TypeError)

    def fastboot(self,devices_name,index):
        """
        重启设备并进入fastboot模式
        :return: reboot_fastboot
        """
        try:
            if devices_name == False:
                pass
            else:
                reboot_fastboot = subprocess.getstatusoutput("adb -s %s reboot bootloader " % (devices_name[index]))[1].replace("\n", "")
                logger.info("设备%s已成功重启设备并进入fastboot模式" % (devices_name[index]))
                return reboot_fastboot
        except Exception as TypeError:
            logger.error(TypeError)


    def get_wifi_state(self,devices_name,index=""):
        """
        获取WiFi连接状态
        :return: wifi_state
        """
        try:
            if devices_name == False:
                pass
            else:
                wifi_state = subprocess.getstatusoutput("adb -s %s shell dumpsys wifi | grep ^Wi-Fi " % (devices_name[index]))[1].replace("\n", "")
                if wifi_state =="Wi-Fi is disabled":
                    logger.error("%s "%(wifi_state))
                    return  False
                else:
                    logger.info("%s " % (wifi_state))
                    return wifi_state
        except Exception as TypeError:
            logger.error(TypeError)

    def get_data_state(self,devices_name,index=""):
        """
        获取移动网络连接状态
        :return: data_state
        """
        try:
            if devices_name == False:
                pass
            else:
                data_state = subprocess.getstatusoutput("adb -s %s shell dumpsys telephony.registry | grep 'mDataConnectionState'" % (devices_name[index]))[1].replace("\n", "")
                return data_state
        except Exception as TypeError:
            logger.error(TypeError)

    def get_network_state(self,devices_name,index=""):
        """
        设备是否连上互联网
        :return:True
        """
        try:
            if devices_name == False:
                pass
            else:
                network_state = subprocess.getstatusoutput("adb -s %s shell ping -w 1 www.baidu.com" % (devices_name[index]))[1].replace("\n", "")
                if "ping: unknown host" in network_state:
                    logger.error("网络未连接！！！")
                else:
                    logger.info("设备已连上互联网：%s " % (network_state))
                    return True
        except Exception as TypeError:
            logger.error(TypeError)

    def call(self, devices_name,index,number):
        """
        拨打电话
        :param index：设备序列
        :param number: 电话号码
        :return:call_info
        """
        try:
            if devices_name == False:
                pass
            else:
                call_info = subprocess.getstatusoutput("adb -s %s shell am start -a android.intent.action.CALL -d tel:%s" % (devices_name[index],number))[1].replace("\n", "")
                logger.info("正在呼叫：%s " % (call_info))
                return call_info
        except Exception as TypeError:
            logger.error(TypeError)

    def open_url(self,devices_name,index,url):
        """
        打开网页
        :return: open_url
        """
        try:
            if devices_name == False:
                pass
            else:
                open_url = subprocess.getstatusoutput("adb -s %s shell am start -a android.intent.action.VIEW -d %s" % (devices_name[index], url))[1].replace("\n", "")
                logger.info("%s " % (open_url))
                return open_url
        except Exception as TypeError:
            logger.error(TypeError)

    def start_application(self, devices_name,package_name,index=""):
        """
        启动一个应用
        :return start_app：开启
        """
        try:
            if devices_name == False:
                pass
            else:
                start_app = subprocess.getstatusoutput("adb -s %s shell am start -n %s" % (devices_name[index], package_name))[1].replace("\n", "")
                logger.info("正在启动：%s " % (package_name))
                return start_app
        except Exception as TypeError:
            logger.error(TypeError)

    def send_keyevent(self, devices_name,index,adb):
        """
        发送一个按键事件即键盘输入
        :param adb：按键按键事件
        :return: send_key
        """
        try:
            if devices_name == False:
                pass
            else:
                send_key = subprocess.getstatusoutput("adb -s %s shell input keyevent %s" % (devices_name[index], adb))[1].replace("\n", "")
                logger.info("正在疯狂输入ing：%s " %(send_key))
                return send_key
        except Exception as TypeError:
            logger.error(TypeError)


    def switch_directory(self,devices_name,filePath=""):
        """
        切换目录(写到一半不想写的def 也不怎么常用到先别引用、先占个位)
        :param devices_name:设备号
        :return: dir_path
        """
        try:
            for dev_name in devices_name:
                switch_dir = subprocess.getstatusoutput("adb -s %s shell cd %s"%(dev_name,filePath))
                logger.info(switch_dir)
        except Exception as TypeError:
            logger.error(TypeError)

if __name__ == '__main__':
    adb = Adb_Manage()
    adb.check_filtered()
    # adb.check_local_file()
    # adb.check_adb_path() #该方法可以不用执行、类部类已操作
    check_devices_status=adb.check_devices_status()
    # adb.uninstall_apk(check_devices_status,package_name="com.tencent.mobileqq")
    adb.install_apk(adb.check_local_file(),check_devices_status,index=0)
    # adb.clear_package(check_devices_status,package_name="com.tencent.mobileqq")
    # adb.get_current_package(check_devices_status)
    # adb.get_battery_info(check_devices_status)
    # adb.remote_connectdev(check_devices_status,adb.get_ipconfig(check_devices_status))
    # adb.create_file(check_devices_status,method="touch",filePath="/sdcard/mkdirtes/test.txt")
    # adb.get_current_package(check_devices_status)
    # adb.file_transfer(check_devices_status,method="remove",source="/sdcard/test.txt")
    # adb.get_process(check_devices_status,keyword="com.tencent.mobileqq")
    # adb.get_screenshot(check_devices_status,source="sdcard")
    # adb.get_ipconfig(check_devices_status)
    # adb.logcat_magement(check_devices_status,method="crash_logcat",filePath = "../Result/Android_Logs/Crash_Logs/")
    # adb.get_device_time(check_devices_status)
    # adb.switch_directory(check_devices_status,filePath="/sdcard")
    # adb.analysis_crash(filePath="../Result/Android_Logs/Crash_Logs/",file_Name="2020-0908-16-55-49-508162-Crash.log")
    # adb.get_phone_info(check_devices_status)
    # while True:
    #     adb.reboot(check_devices_status)
    # adb.file_exists(check_devices_status,target="/sdcard")
    # while True:
    #     time.sleep(3)
    #     if adb.is_install(check_devices_status, package_name="com.tencent.mobileqq") ==False:
    #         logger.info("Installing！！！")
    #         adb.install_apk(adb.check_local_file(),check_devices_status,index=0)
    #     else:
    #         logger.info("UnInstalling！！！")
    #         adb.uninstall_apk(check_devices_status,package_name="com.tencent.mobileqq")
    # adb.get_ps_pid(check_devices_status, package_name="com.tencent.mobileqq:MSF", index=0)
    # adb.kill_process(check_devices_status, index=0,pid=adb.get_ps_pid(check_devices_status, keyword="com.tencent.mobileqq:MSF", index=0))
    # adb.quit_app(check_devices_status,package_name="com.tencent.mobileqq",index=0)
    # adb.recovery(check_devices_status,index=0)
    # adb.fastboot(check_devices_status, index=0)
    # adb.get_wifi_state(check_devices_status,index=0)
    # adb.get_data_state(check_devices_status,index=0)
    # adb.get_network_state(check_devices_status,index=0)
    # # adb.call(check_devices_status,index=0,number=501893067)
    # adb.open_url(check_devices_status,index=0,url="https://www.baidu.com")
    # adb.start_application(check_devices_status,index=0,package_name="com.tencent.mobileqq")
    # adb.send_keyevent(check_devices_status,index=0,keyCode=10)
    # adb.filtered()
