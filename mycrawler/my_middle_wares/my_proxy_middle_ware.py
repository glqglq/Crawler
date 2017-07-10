# -*- coding: utf-8 -*-

import time
import random
import logging
import redis

from ..settings import BOT_NAME,REDIS_URL
from ..util.distributed_lock import dist_lock

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class RandomProxy(object):
    def __init__(self, settings):
        self.enable_proxy = settings.get('ENABLE_PROXY')
        self.proxies = {}
        self.server = redis.StrictRedis.from_url(REDIS_URL)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if self.enable_proxy:

            # 从redis中获取一个ip

            while True:
                with dist_lock(BOT_NAME, self.server):
                    self.proxies = self.server.hgetall('%s:proxy_pool'%BOT_NAME)
                if self.proxies.has_key('running'):
                   del self.proxies['running']
                if self.proxies:
                    break
                time.sleep(0.5)

            # 对于新闻博客类，随机选个代理
            proxy_address = random.choice(list(self.proxies.keys()))
            if request.meta.get("type",None) == 0:
                request.meta['proxy'] = proxy_address