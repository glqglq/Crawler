# -*- coding: utf-8 -*-

import re,chardet,redis,sys,threading,jieba

from mycrawler.util.jparser import PageModel
from scrapy_redis.spiders import RedisSpider
from ..items.items import MyCrawlerItem
from ..util import url_cleaning
from ..settings import REDIS_URL,BOT_NAME,ENABLE_PROXY
from scrapy import Request
from ..util.get_proxy import get_proxy
from ..util.summary import Reduction



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

        self.server = redis.StrictRedis.from_url(REDIS_URL)
        serv  = self.server
        #开个线程，不断获取proxy
        if ENABLE_PROXY:
            self.get_proxy_threading = threading.Thread(target=get_proxy,args=(serv,))
            self.get_proxy_threading.setDaemon(True)
            self.get_proxy_threading.start()

        self.reduction = Reduction()



    #     if kwargs:
    #         #DONE 初始start_urls加入爬取队列：
    #         self.json = eval(kwargs["json"])
    #         self.start_server = redis.StrictRedis.from_url(REDIS_URL)
    #         for task in self.json.keys():
    #             self.start_server.lpush('%s:start_urls'%BOT_NAME,task)

    # def make_requests_from_url(self, url):
    #     return get_message_from_json(url,self.json)

    def parse(self, response):

        #应对不同网站的不同编码
        content_type = chardet.detect(response.body)
        if content_type['encoding'] != 'UTF-8':
            body = response.body.decode(content_type['encoding'])
        body = body.encode('utf-8')
        # body = response.body.decode("unicode_escape")

        # DONE 抽取该页新的url并清洗
        pattern = re.compile(r'href=\".*?\"',re.M)
        urls = pattern.findall(body)
        urls = url_cleaning.all_url_cleaning(self.server,response,urls)
        # print 'haha'
        item = MyCrawlerItem()
        item['url'] = response.url
        item['id'] = response.meta["id"]

        this_task_information = eval(self.server.hget('%s:task_information' % BOT_NAME, response.meta["id"]))


        # DONE 新闻博客类抽取整页
        if this_task_information["type"] == 0:

            #DONE 网页正文的自动抽取
            result_body = PageModel(body).extract()
            result_body_temp = ''
            for x in result_body['content']:
                if x['type'] == 'text':
                    result_body_temp = result_body_temp.join(x['data'])

            # DONE 自动摘要
            result_body_summary = self.reduction.reduce(result_body_temp, 1.0)[0]

            # DONE 关键词提取，取5个关键词，返回list
            result_body_keywords = jieba.analyse.extract_tags(result_body_temp, topK=5)

            item['type'] = 0
            item['content'] = str({'content':result_body_temp,'summary':result_body_summary,'keywords':result_body_keywords})
            item['this_url_rule'] = ''


        # DONE 电商类抽取部分结构化好的商品信息
        elif this_task_information["type"] == 1 and response.meta.has_key('fetcheditemcontents') and response.meta['fetcheditemcontents']:
            item['type'] = 1
            item['content'] = response.meta["fetcheditemcontents"]
            item['this_url_rule'] = response.meta['this_url_rule']
        #未识别类型
        else:
            item['type'] = -1
            item['content'] = ''

        if item['type'] != -1:
            yield item


        #DONE 将符合条件的链接加到待爬取队列中去，传递meta
        for url in urls:
            if this_task_information["type"] == 1:
                this_url_priority = this_task_information["priority"]
                this_url_rule = ''

                # 识别特殊页面，设置优先级+1和this_url_rule
                if this_task_information.has_key("rules") and this_task_information["rules"]:
                    for rule in this_task_information["rules"].keys():
                        if re.compile(rule).match(url):
                            this_url_rule = rule
                            this_url_priority += 1

                # meta中共两项：id、this_url_rule
                clean_meta = {}
                clean_meta["id"] = response.meta["id"]
                clean_meta["this_url_rule"] = this_url_rule
                yield Request(url, priority=this_url_priority, meta=clean_meta)
            else:
                # meta中共一项：id
                yield Request(url, priority=this_task_information["priority"], meta=response.meta)