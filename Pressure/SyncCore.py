# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : SyncCore.py
@Author: v_yanqyu
@Desc  :
@Date  : 2020/10/16 21:22
'''
import time
from Pressure import PrintPlt
from Pressure import SyncRequest
from Logger.GlobalLog import Logger
logger = Logger.write_log()

# 请求池
syncPool = []
round_count = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SPN-AL00 Build/HUAWEISPN-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045410 Mobile Safari/537.36 Now/1.54.5_9 NetType/WIFI',
    'Accept': 'text/html,application/xhtml xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Connection': 'close',
    'q-ua2':'QV=3&PL=ADR&PR=TRD&PP=com.tencent.now&PPVN=1.54.5_DEBUG_TASK_ID:115&TBSVC=43963&CO=BK&COVC=045410&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= SPN-AL00 &RL=1080*2232&OS=9&API=28',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookies0':'accessToken=8C62ADD399E162843A7168A7D79C1AB9; access_token=null; openid=D0F677F152C6B978D5189F4AC53A2075; openId=D0F677F152C6B978D5189F4AC53A2075; ilive_uin=501893067; ilive_tinyid=144115198843602958; versioncode=2500; client_type=401; clientid=YjQzNzcxNzhhMzQ5ZmY5Mg==; clientqid=YmJkYjk3ODhiMTg5MWU2MDM2NTY5NzJlMTAwMDFiYjE0OTE3; login_type=18; ilive_a2=d4e2bf395bebdd7147248f09a573dfc3e5817f98cc2e940fb86cc03a5998fce586ac919cf28ac97335ed7d513596cc7ea4efc914ed1c346223e5f7d276ae5b6fd818d794f10031d2; ilive_type=1; original_id=D0F677F152C6B978D5189F4AC53A2075; original_key=8C62ADD399E162843A7168A7D79C1AB9; original_key_type=37; __client_exchange_appid=1450006664; wx87f0d936dd720581_now_openid=D0F677F152C6B978D5189F4AC53A2075; _fst_id=38; _supWebp=1'
}


def init(count, url, methods='GET', params='{}', read=False):
    start_time = time.time()
    logger.info('开始预创建请求池....')
    if read:
        for requestId in range(count):
            # dataList = data.request_data[requestId]
            # if utils.check_json(str(dataList[0]).replace("'", "")):
            #     params = json.loads(str(dataList[0]).replace("'", ""))
            # else:
            #     logger.error('json数据格式错误 跳过构建该请求')
            #     continue
            request = SyncRequest.SyncRequestTask(requestId, url, methods, params, headers)
            syncPool.append(request)
    else:
        for requestId in range(count):
            request = SyncRequest.SyncRequestTask(requestId, url, methods, params, headers)
            syncPool.append(request)
    logger.info("初始化消耗时间 {:.2f} 豪秒".format((time.time() - start_time) * 1000))

# 这里id代表是第几次调用从0开始
def fast_run(begin, end):
    logger.warning("开始index{} 结束index{}".format(begin, end))
    run_start_time = time.time()
    logger.info('开始发起快速异步请求....')
    for request in syncPool[int(begin):int(end)]:
        request.start()
    logger.warning("请求消耗时间 {:.2f} 豪秒".format((time.time() - run_start_time) * 1000))


def slow_run(begin, end, slowTime):
    logger.warning("开始index{} 结束index{}".format(begin, end))
    run_start_time = time.time()
    logger.info('开始发起慢速异步请求....')
    if slowTime == 0:
        fast_run(begin, end)
    else:
        waitTime = round(((slowTime * 1000) / len(syncPool)) / 1000, 3)
        logger.info("延迟时间为{}毫秒".format(waitTime * 1000))
        for request in syncPool[int(begin):int(end)]:
            request.start()
            time.sleep(waitTime)
    logger.warning("请求消耗时间 {} 豪秒".format((time.time() - run_start_time) * 1000))

def join(begin, end):
    for request in syncPool[int(begin):int(end)]:
        request.join()

def out(length):
    logger.warning("总请求次数 {int(length)} 次")
    logger.warning("成功请求 {len(SyncRequest.success)} 次")
    logger.warning("失败请求 {len(SyncRequest.fail)} 次")
    logger.warning("限流请求 {SyncRequest.limit} 次")
    logger.warning("成功率 {:.2f} %".format((len(SyncRequest.success) / int(length)) * 100))
    logger.warning("失败率 {:.2f} %".format((len(SyncRequest.fail) / int(length)) * 100))
    logger.warning("限流百分比 {:.2f} %".format(SyncRequest.limit / int(length) * 100))
    logger.warning("最长请求时间 {:.2f} 毫秒".format(max(SyncRequest.response_time)))
    logger.warning("最短请求时间 {:.2f} 毫秒".format(min(SyncRequest.response_time)))
    logger.warning("平均请求时间 {:.2f} 毫秒".format(sum(SyncRequest.response_time) / len(SyncRequest.response_time)))
    # 打印成功请求的request中信息
    for success in SyncRequest.success:
        logger.debug(success.content)
    # 打印失败请求的request中信息
    for fail in SyncRequest.fail:
        if fail is not None:
            logger.debug(fail.content)


def switch_start(flag, slowTime, id):
    step = len(syncPool) / round_count
    begin = id * step
    if flag is True:
        fast_run(begin, begin + step)
    else:
        slow_run(begin, begin + step, slowTime)
    join(begin, begin + step)
    out(begin + step)
    generate_chart(id)
    # syncPool.clear()


def start(slowTime, roundCount, thread_count, request_url, method, param, read=False):
    logger.warning("共需要执行次数 {roundCount}")

    if roundCount > 1:
        global round_count
        round_count = roundCount

    init(thread_count * roundCount, request_url, str(method).upper(), param, read)
    if slowTime == 0:
        for count in range(roundCount):
            logger.warning("当前执行次数 {count + 1}")
            switch_start(True, 0, count)
    else:
        for count in range(roundCount):
            logger.warning("当前执行次数 {count + 1}")
            switch_start(False, slowTime, count)


def generate_chart(id):
    PrintPlt.show_bar(id)
    PrintPlt.show_pie(id)