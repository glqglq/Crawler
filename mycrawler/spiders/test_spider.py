# -*- coding: utf-8 -*-

import re

import redis
from scrapy_redis.spiders import RedisSpider
from ..items.items import MyCrawlerItem
from ..util import url_cleaning
from ..settings import REDIS_URL,BOT_NAME
from scrapy import Request
from ..util.get_proxy import get_proxy

import sys,threading

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
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

        #开个线程，不断获取proxy
        self.get_proxy_threading = threading.Thread(target=get_proxy,args=())
        self.get_proxy_threading.setDaemon(True)
        self.get_proxy_threading.start()
    #     if kwargs:
    #         #DONE 初始start_urls加入爬取队列：
    #         self.json = eval(kwargs["json"])
    #         self.start_server = redis.StrictRedis.from_url(REDIS_URL)
    #         for task in self.json.keys():
    #             self.start_server.lpush('%s:start_urls'%BOT_NAME,task)

    # def make_requests_from_url(self, url):
    #     return get_message_from_json(url,self.json)

    def parse(self, response):

        # DONE 抽取该页新的url并清洗
        body = response.body
        pattern = re.compile(r'href=\".*?\"',re.M)
        urls = pattern.findall(body)
        urls = url_cleaning.all_url_cleaning(response,urls)
        # print 'haha'
        item = MyCrawlerItem()
        item['url'] = response.url
        # DONE 新闻博客类抽取整页
        if response.meta["type"] == 0:
            item['type'] = 0
            item['content'] = body.decode("unicode_escape")

        # DONE 电商类抽取部分结构化好的商品信息
        elif response.meta["type"] == 1 and response.meta.has_key('fetcheditemcontents'):
            item['type'] = 1
            item['content'] = response.meta["fetcheditemcontents"]
        #未识别类型
        else:
            item['type'] = -1
            item['content'] = ''

        yield item

        #DONE 将符合条件的链接加到待爬取队列中去，传递meta
        for url in urls:
        #     # yield get_message_from_response(url,response)
            if response.meta["type"] == 1:
                this_url_priority = response.meta["priority"]
                this_url_rule = ''

                # 识别特殊页面，设置优先级和
                if response.meta.has_key("rules") and response.meta["rules"]:
                    for rule in response.meta["rules"].keys():
                        if re.compile(rule).match(url):
                            this_url_rule = rule
                            # 详情页，优先级增加
                            this_url_priority += 1

                # meta中共五项：priority、type、alloweddomains、this_url_rule、rules
                clean_meta = response.meta
                clean_meta["this_url_rule"] = this_url_rule
                yield Request(url, priority=this_url_priority, meta=clean_meta)
            else:
                yield Request(url, priority=response.meta["priority"], meta=response.meta)