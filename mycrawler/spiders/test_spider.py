# -*- coding: utf-8 -*-

import re
from scrapy_redis.spiders import RedisSpider
from ..items.items import MyCrawlerItem
from scrapy import Request

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class test_spider(RedisSpider):

    name = "mycrawler"
    # download_delay = 2

    # start_urls = [r"https://taobao.com"]
    # custom_settings = #在爬虫运行时覆盖来自settings的设置

    # redis_key = 'mycrawler:start_urls'  #redis中要有主键为mycrawler:start_urls的list，没有的话爬虫只能监听等待

    def __init__(self):
        self.allowed_domains = [r"ict.ac.cn", r"ict.cas.cn"]

    def url_cleaning2(self,url):
        for domain in self.allowed_domains:
            if domain in url and '@' not in url:
                return True
        return False

    def url_cleaning(self,url):
        # DONE 清洗从页面提取出来的单个url
        url = url[6:-1]
        url = url.strip(r'/')
        if r'https://' in url:
            url = url[8:]
        # print url
        return url

    def url_cleaning3(self,url):
        if r'http://'not in url:
            url = 'http://' + url
        url = url.strip(r'/')
        return url

    def parse(self, response):
        body = response.body
        url_now = response.url
        # print body
        pattern = re.compile(r'href=\".*?\"',re.M)
        urls = pattern.findall(body)


        urls = map(self.url_cleaning,urls)
        for i in range(len(urls)):
            if urls[i][0] == '.' and urls[i][1] == r'/':
                urls[i] = url_now + urls[i][1:]
            elif urls[i][0] == '.' and urls[i][1] != r'/':
                urls[i] = url_now + r'/' + urls[i][1:]
        urls = map(self.url_cleaning3,urls)
        urls = filter(self.url_cleaning2,urls)

        # print urls
        # print '============================================'

        #DONE Item处理
        item = MyCrawlerItem()
        item['url'] = response.url
        item['content'] = body
        # print body
        yield item

        #DONE 将符合条件的链接加到待爬取队列中去
        for url in urls:
            yield Request(url)