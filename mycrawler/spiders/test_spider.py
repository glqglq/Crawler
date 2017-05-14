# -*- coding: utf-8 -*-

import re
from scrapy_redis.spiders import RedisSpider
from ..items.items import MyCrawlerItem
from scrapy import Request
from ..util import url_cleaning
from ..util.get_priority import get_priority

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class test_spider(RedisSpider):

    name = "mycrawler"
    # download_delay = 2

    # start_urls = [r"https://taobao.com"]
    # custom_settings = #在爬虫运行时覆盖来自settings的设置

    # redis_key = 'mycrawler:start_urls'  #redis中要有主键为mycrawler:start_urls的list，没有的话爬虫只能监听等待

    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        # self.json =

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield self.make_requests_from_url(url)
    #
    # def make_requests_from_url(self, url):
    #     return Request(url, meta = self.json,priority=json)

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
            yield Request(url,priority=get_priority(url))