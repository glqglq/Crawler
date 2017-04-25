# -*- coding: utf-8 -*-

import scrapy,re,random
from scrapy_splash import SplashRequest
from scrapy import Request

class test_spider(scrapy.Spider):
    name = "taobao"
    allowed_domains = [r"ip5.me"]
    start_urls = [r"http://ip5.me"]

    def start_requests(self):
        #DONE js动态页面抓取发送request
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 1})
            # yield Request(url,self.parse)
        # TODO 静态页面抓取发送request

    def parse(self, response):
        # DONE 用正则表达式将本页所有链接提取出来
        body = response.body.decode('utf-8')
        print body
        pattern = re.compile(r'href=\".*?\"',re.M)
        urls = pattern.findall(body)

        #DONE 将urls进行清洗
        urls = map(self.url_cleaning,urls)
        # for url in urls:
        #      print url

        #TODO 将符合条件的链接加到待爬取队列中去

    def url_cleaning(self,url):
        "清洗从页面提取出来的url"
        #TODO 清洗从页面提取出来的单个url
        url = url[6:-1]
        return url