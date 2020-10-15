# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  : SyncRequest.py
@Author: v_yanqyu
@Desc  : 
@Date  : 2020/10/16 21:21
'''
import threading
import time
import json
import requests
from threading import Lock
from Logger.GlobalLog import Logger
logger = Logger.write_log()

sessions = requests.sessions
sessions.HTTPAdapter.max_retries = 5
lock = Lock()
success = []
fail = []
limit = 0
response_time = []
ids = []

def data_build(id, ms):
    logger.info('ID {} 响应 {:.2f} 毫秒'.format(id, ms * 1000))
    ids.append(id)
    response_time.append(ms * 1000)


class SyncRequestTask(threading.Thread):

    def __init__(self, threadId, url, method, params, header, timeout=10):
        threading.Thread.__init__(self)
        self.setName("进程ID：%s"%(threadId))
        self.url = url
        self.method = method
        self.params = params
        self.timeout = timeout
        self.header = header

    # 发送请求
    def request(self):
        req = None
        try:
            if self.method == 'GET':
                req = self.doGet()
                self.add(req)
            else:
                req = self.doPost()
                self.add(req)
        except Exception as e:
            print(e)
            fail.append(req)

    def doGet(self):
        startTime = time.time()

        s = sessions.session()
        req = s.get(self.url, headers=self.header, timeout=self.timeout)
        data_build(self.getName(), time.time() - startTime)
        req.close()
        return req

    def doPost(self):
        # request_body = json.dumps(self.params)
        s = sessions.session()
        startTime = time.time()
        req = s.post(self.url, data=self.params, headers=self.header, timeout=self.timeout)
        data_build(self.getName(), time.time() - startTime)
        req.close()
        return req,req.status_code

    @staticmethod
    def add(request):
        global lock
        global limit
        lock.acquire()
        if request.status_code == 200:
            success.append(request)
        elif request.status_code == 429:
            limit += 1
        else:
            fail.append(request)
        lock.release()

    def run(self):
        # 开始发送请求
        self.request()
