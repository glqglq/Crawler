# -*- coding: utf-8 -*-

import redis,urllib2,random

from scrapy.selector import Selector

server = redis.StrictRedis.from_url(r'redis://admin:1@192.168.28.134:6379')
while True:
    try:
        proxies = list(server.hgetall('mycrawler:proxy_pool').keys())
        proxy = random.choice(proxies)

        proxy_handler = urllib2.ProxyHandler({'http': "http://" + proxy})
        opener = urllib2.build_opener(proxy_handler)
        response = opener.open(r'http://www.ip002.net/')
        assert response.code == 200
        s = Selector(text = response.read())
        print s.xpath(r'/html/body/div[2]/div/strong/div[1]').extract()[0]
        # print 'OK'
    except:
        print '不好使'