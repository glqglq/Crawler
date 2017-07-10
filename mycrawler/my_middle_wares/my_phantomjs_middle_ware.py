# -*- coding: utf-8 -*-
import random
import time
import redis

from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from mycrawler.util.distributed_lock import dist_lock
from ..settings import BOT_NAME

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class PhantomjsMiddleware(object):
    def __init__(self,user_agents,enable_proxy,redis_url,enable_phantomjs):
        #取ua列表
        self.user_agents = user_agents

        # 取proxy列表
        self.enable_proxy = enable_proxy
        self.proxies = {}

        self.server = redis.StrictRedis.from_url(redis_url)

        #phantomjs相关设置
        self.enable_phantomjs = enable_phantomjs
        self.dcap = dict(DesiredCapabilities.PHANTOMJS)
        self.dcap["phantomjs.page.settings.disk-cache"] = True
        self.dcap["phantomjs.page.settings.loadImages"] = False
        # self.js = "var i=1;window.setInterval(a, 50);function a(){document.getElementsByTagName('body')[0].scrollTop=100*i;i++;}"

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENTS'],crawler.settings['ENABLE_PROXY'],crawler.settings['REDIS_URL'],crawler.settings['ENABLE_PHANTOMJS'])
        return o

    def process_request(self, request, spider):
        if self.enable_phantomjs:

            with dist_lock(BOT_NAME,self.server):
                this_task_information = eval(self.server.hget('%s:task_information'%BOT_NAME,request.meta.get("id",None)))

            if this_task_information.get('type',None) == 1 and request.meta.has_key("this_url_rule"):#如果想对eb类网站全体用phantomjs的话，就把这个has_key去掉

                # 定义初始设置
                self.service_args = []
                self.service_args.append('--ignore-ssl-errors=true')  ##忽略https错误

                # 随机定义代理
                if self.enable_proxy:
                    while True:
                        with dist_lock(BOT_NAME, self.server):
                            self.proxies = self.server.hgetall('%s:proxy_pool' % BOT_NAME)
                        if self.proxies.has_key('running'):
                            del self.proxies['running']
                        if self.proxies:
                            break
                        time.sleep(0.5)
                    self.service_args.append('--proxy=%s' % random.choice(self.proxies.keys()))


                #随机定义UA
                self.dcap["phantomjs.page.settings.userAgent"] = random.choice(self.user_agents)

                #开启headless浏览器并进行初始请求
                driver = webdriver.PhantomJS(service_args = self.service_args, desired_capabilities=self.dcap)
                driver.set_window_size(1500, 15000)
                driver.get(request.url.replace(';','&'))
                page_source = driver.page_source

                driver.close()
                return HtmlResponse(request.url, status=200, body=page_source, encoding='utf-8', request=request)

            # DONE 等待评论按钮加载出来，并按下，
            if_found_button = 0
            # try:
            #     WebDriverWait(self.driver, 3, 0.5).until(EC.presence_of_element_located((self.get_type(request.meta["rules"][this_url_rule]["comment_button_type"]),request.meta["rules"][this_url_rule]["comment_button_content"])))
            #     press_button(self.driver,request.meta["rules"][this_url_rule]["comment_button_type"],request.meta["rules"][this_url_rule]["comment_button_content"])
            #     if_found_button = 1
            # except TimeoutException,e:
            #     #评论按钮找不到
            #     pass

            # if if_found_button == 1:
            #     # TODO 成功按下后抓取评论区：不断等待下一页按钮加载进来，并按下。换掉这种sb的加载方式，自己算多少页
            #     pass
                # try:
                #     while True:
                #         # 抓取本页内容，存入meta：
                #         # 对加载进来的内容进行处理（解析、保存），写个回调函数
                #         getconmmentcontent(self.driver.page_source, request.meta["rules"][this_url_rule])
                #         WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located((self.next_page_button_type,self.next_page_button_content)))
                #         press_button(self.driver,request.meta["rules"][this_url_rule]["comment_button_type"],request.meta["rules"][request.meta["this_url_rule"]]["comment_button_content"])
                # except TimeoutException,e:
                #     print '%s 评论区抓取完毕'%url

                #抓取商品详情内容，抓取回来的内容加入到request,meta中去




    def process_response(self, request, response, spider):
        if len(response.body) == 100:
            return IgnoreRequest("body length == 100")
        else:
            return response

    # def get_type(self,type_num):
    #     if type_num == 0:
    #         return By.XPATH
    #     elif type_num == 1:
    #         return By.CLASS_NAME
    #     elif type_num == 2:
    #         return By.CSS_SELECTOR
    #     elif type_num == 3:
    #         return By.ID
    #     elif type_num == 4:
    #         return By.LINK_TEXT
    #     elif type_num == 5:
    #         return By.NAME
    #     elif type_num == 6:
    #         return By.TAG_NAME

    # def __del__(self):
    #     self.driver.quit()