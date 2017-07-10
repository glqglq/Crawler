# -*- coding: utf-8 -*-
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class UserAgentMiddleWare(object):
    '''ua池'''
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENTS'])
        return o

    def process_request(self, request, spider):

        # 随机选择user-agent
        ua = random.choice(self.user_agent)
        try:
            request.headers.setdefault(b'User-Agent', ua)
        except Exception,e:
            print e