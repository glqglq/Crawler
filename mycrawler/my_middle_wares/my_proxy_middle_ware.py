# -*- coding: utf-8 -*-

import re
import random
import logging

from ..settings import ENABLE_JS

log = logging.getLogger('scrapy.proxies')




class RandomProxy(object):
    def __init__(self, settings):
        self.proxy_list = settings.get('PROXY_LIST')
        if self.proxy_list is None:
            raise KeyError('PROXY_LIST setting is missing')

        fin = open(self.proxy_list)
        self.proxies = {}
        for line in fin.readlines():
            parts = re.match('(\w+://)(\w+:\w+@)?(.+)', line.strip())
            if not parts:
                continue

            # Cut trailing @
            if parts.group(2):
                user_pass = parts.group(2)[:-1]
            else:
                user_pass = ''

            self.proxies[parts.group(1) + parts.group(3)] = user_pass
        fin.close()


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            if request.meta["exception"] is False:
                return
        request.meta["exception"] = False
        if len(self.proxies) == 0:
            raise ValueError('All proxies are unusable, cannot proceed')

        proxy_address = random.choice(list(self.proxies.keys()))
        if ENABLE_JS == False:
            request.meta['proxy'] = proxy_address
            log.debug('Using proxy <%s>, %d proxies left' % (
                proxy_address, len(self.proxies) - 1))

    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return
        proxy = request.meta['proxy']
        try:
            del self.proxies[proxy]
        except KeyError:
            pass
        request.meta["exception"] = True
        log.info('Removing failed proxy <%s>, %d proxies left' % (
            proxy, len(self.proxies)))
