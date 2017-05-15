# -*- coding: utf-8 -*-

import re

import redis
from scrapy_redis.spiders import RedisSpider
from scrapy import Request
from ..items.items import MyCrawlerItem
from ..util import url_cleaning
from ..settings import REDIS_URL,BOT_NAME
from ..util.get_messge import get_message_from_response

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class test_spider(RedisSpider):

    name = "mycrawler"
    # download_delay = 2

    # start_urls = [r"https://taobao.com"]
    # custom_settings = #在爬虫运行时覆盖来自settings的设置

    # redis_key = 'mycrawler:start_urls'  #redis中要有主键为mycrawler:start_urls的list，没有的话爬虫只能监听等待

    # def __init__(self, name=None, **kwargs):
    #     if name is not None:
    #         self.name = name
    #     elif not getattr(self, 'name', None):
    #         raise ValueError("%s must have a name" % type(self).__name__)
    #     self.__dict__.update(kwargs)
    #     if not hasattr(self, 'start_urls'):
    #         self.start_urls = []
    #     if kwargs:
    #         #DONE 初始start_urls加入爬取队列：
    #         self.json = eval(kwargs["json"])
    #         self.start_server = redis.StrictRedis.from_url(REDIS_URL)
    #         for task in self.json.keys():
    #             self.start_server.lpush('%s:start_urls'%BOT_NAME,task)

    # def make_requests_from_url(self, url):
    #     return get_message_from_json(url,self.json)

    def parse(self, response):
        body = response.body
        url_now = response.url
        # print body
        pattern = re.compile(r'href=\".*?\"',re.M)
        urls = pattern.findall(body)

        urls = url_cleaning.all_url_cleaning(url_now,urls)

        #DONE Item处理
        item = MyCrawlerItem()
        item['url'] = response.url
        item['content'] = body.decode("unicode_escape")
        # print body
        yield item

        # #DONE 将符合条件的链接加到待爬取队列中去
        for url in urls:
            # Request(url)
            yield get_message_from_response(url,response)