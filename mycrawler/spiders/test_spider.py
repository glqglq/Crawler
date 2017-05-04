# -*- coding: utf-8 -*-

import re
from scrapy_redis.spiders import RedisSpider
from ..items.items import MyCrawlerItem
from ..settings import ENABLE_JS
from scrapy import Request

class test_spider(RedisSpider):
    name = "mycrawler"
    download_delay = 2
    allowed_domains = [r"taobao.com"]
    # start_urls = [r"https://taobao.com"]
    # custom_settings = #在爬虫运行时覆盖来自settings的设置

    # redis_key = 'mycrawler:start_urls'  #redis中要有主键为mycrawler:start_urls的list，没有的话爬虫只能监听等待

    def url_cleaning2(self,url):
        for domain in self.allowed_domains:
            if domain in url:
                return True
        return False

    def url_cleaning(self,url):
        # DONE 清洗从页面提取出来的单个url
        url = url[6:-1]
        url = url.strip(r'/')
        if u'https://' in url:
            url = url[8:]
        if u'http://'not in url:
            url = 'http://' + url
        # print url
        return url

    def parse(self, response):
        body = response.body.decode('utf-8')
        # print body
        pattern = re.compile(r'href=\".*?\"',re.M)
        urls = pattern.findall(body)
        urls = filter(self.url_cleaning2,urls)
        urls = map(self.url_cleaning,urls)

        #DONE Item处理
        item = MyCrawlerItem()
        item['url'] = response.url.decode('utf-8').encode('utf-8')
        item['content'] = body.encode('utf-8')
        # print body
        yield item

        #DONE 将符合条件的链接加到待爬取队列中去
        for url in urls:
            yield Request(url)