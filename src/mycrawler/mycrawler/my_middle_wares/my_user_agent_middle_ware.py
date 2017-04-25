# -*- coding: utf-8 -*-
import random
from scrapy import signals

class UserAgentMiddleWare(object):
    '''ua池'''
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENTS'])
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent', self.user_agent)

    def process_request(self, request, spider):
        # 随机选择user-agent
        ua = random.choice(self.user_agent)
        try:
            request.headers.setdefault(b'User-Agent', ua)
        except Exception,e:
            print e
        print '当前使用的user-agent是' +  request.headers.get(b'User-Agent')