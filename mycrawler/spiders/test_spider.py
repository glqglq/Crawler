# -*- coding: utf-8 -*-

import re,chardet,redis,sys,threading,jieba.analyse

from mycrawler.util.jparser import PageModel
from scrapy_redis.spiders import RedisSpider
from scrapy import Request
from ..items.items import MyCrawlerItem
from ..util import url_cleaning
from ..settings import REDIS_URL,BOT_NAME,ENABLE_PROXY
from ..util.get_proxy import get_proxy
from ..util.distributed_lock import dist_lock
from ..util.get_json_page_content import getitemcontent

reload(sys)
sys.setdefaultencoding('utf-8')


class test_spider(RedisSpider):

    name = "mycrawler"

    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

        # redis连接
        self.server = redis.StrictRedis.from_url(REDIS_URL)
        serv  = self.server

        # 开个线程，不断获取proxy
        if ENABLE_PROXY:
            self.get_proxy_threading = threading.Thread(target=get_proxy,args=(serv,))
            self.get_proxy_threading.setDaemon(True)  #主线程执行完毕回收子线程
            self.get_proxy_threading.start()

        # pattern of re
        self.pattern = re.compile(r'href=\".*?\"', re.M)

    def parse(self, response):

        #应对不同网站的不同编码，将爬取内容转为unicode，再转为utf-8
        content_type = chardet.detect(response.body)
        if content_type.get('encoding','UTF-8') != 'UTF-8':
            body = response.body.decode(content_type['encoding'])  #将某些编码内容转为unicode

        # DONE 抽取该页新的url并清洗
        urls = self.pattern.findall(body)
        urls = url_cleaning.all_url_cleaning(self.server,response,urls)

        # 构建基础item
        item = MyCrawlerItem()
        item['url'] = response.url
        item['id'] = response.meta.get("id",None)

        # 获取任务task_information的json
        this_url_rule = None
        if response.meta.has_key('id'):
            with dist_lock(BOT_NAME, self.server):
                this_task_information = eval(self.server.hget('%s:task_information' % BOT_NAME, response.meta["id"]))

        # DONE 新闻博客类抽取正文、关键词
        if this_task_information.get("type",None) == 0:

            #DONE 网页正文、摘要的自动抽取
            result_body = PageModel(body).extract()
            result_body_temp = ''
            for x in result_body.get('content',None):
                if x.get('type',None) == 'text':
                    result_body_temp += x.get('data',None)
            result_body_temp = result_body_temp.encode('utf-8')#unicode转utf-8
            result_summary_temp = result_body.get('title',None)

            # DONE 关键词提取，取4个关键词，返回list
            result_body_keywords = jieba.analyse.extract_tags(result_body_temp, topK=4)

            item['type'] = 0
            item['content'] = {'content':result_body_temp,'summary':result_summary_temp,'keywords':result_body_keywords}
            item['this_url_rule'] = ''


        # DONE 电商类抽取部分结构化好的商品信息
        elif this_task_information["type"] == 1:

            this_url_rule = response.meta.get("this_url_rule",None)
            if this_task_information.has_key('rules'):
                rules = this_task_information["rules"][this_url_rule]["itemcontents"]

            item['type'] = 1
            item['content'] = getitemcontent(response.body, rules)
            item['this_url_rule'] = response.meta.get('this_url_rule',None)

        #未识别类型
        else:
            item['type'] = -1
            item['content'] = ''

        if item['type'] != -1:
            yield item


        #DONE 将符合条件的链接加到待爬取队列中去，传递meta
        for url in urls:
            if this_task_information.get("type",None) == 1:
                this_url_priority = this_task_information.get("priority",None)
                this_url_rule = ''

                # 识别特殊页面，设置优先级+1和this_url_rule
                if this_task_information.get("rules",None):
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
                yield Request(url, priority=this_task_information.get("priority",None), meta=response.meta)