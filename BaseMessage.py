import requests
import core
import re
import time
from Wappalyzer import WebPage
import get_message
import ImportToRedis
import redis


'''
获取输入网址基础信息:
    1,WEB指纹识别,技术识别 Finger 
    2,状态码 Status
    3,标题 Title
    4,收录扫描时间 Date
    5,响应包 response
    6,端口开放信息
    
'''


class GetBaseMessage():
    def __init__(self, url, redispool):
        print("hi!")
        self.domain = url
        self.redispool = redispool
        try:
            if not (url.startswith("http://") or url.startswith("https://")):
                self.url = "http://" + url
            else:
                self.url = url
            self.rep = requests.get(self.url, headers=core.GetHeaders(), timeout=5, verify=False)
        except:
            self.rep = None
            pass
        if self.rep == None:
            try:
                self.url = "https://" + url
                self.rep = requests.get(self.url, headers=core.GetHeaders(), timeout=5, verify=False)
            except:
                pass

    def GetStatus(self):
        return str(self.rep.status_code)

    def GetTitle(self):
        if self.rep != None:
            return re.findall('<title>(.*?)</title>', self.rep.text)[0]
        return None

    def GetDate(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def GetResponseHeader(self):
        context=""
        for key, val in self.rep.headers.items():
            context += (key + ": " + val + "\r\n")
        return context

    def GetFinger(self):
        return WebPage(self.url, self.rep).info()

    def PortScan(self):
        return get_message.PortScan(self.domain)

    def SenDir(self):
        return get_message.SenFileScan(self.domain, self.redispool)


if __name__=='__main__':
    # redispool=redis.ConnectionPool(host='127.0.0.1',port=6379, decode_responses=True)
    redispool = redis.Redis(connection_pool=ImportToRedis.redisPool)
    try:
        test=GetBaseMessage("test.vulnweb.com",redispool)
        print(test.GetStatus())
        print(test.GetTitle())
        print(test.GetDate())
        print(test.GetResponseHeader())
        print(test.GetFinger())
        print(test.PortScan())
        print(test.SenDir())

    except Exception as e:
        print(e)
        pass

