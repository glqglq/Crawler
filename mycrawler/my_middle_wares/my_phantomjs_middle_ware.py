# -*- coding: utf-8 -*-
import random
import time
import redis
import chardet

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from mycrawler.util.distributed_lock import dist_lock
from ..settings import BOT_NAME

from ..util.get_json_page_content import getitemcontent

"""
    爬取电商网站时启用该middleware
    三种页面：
        普通页面
        列表页面（需要翻页）
        详情页面（需要提取内容+翻页）
"""


class PhantomjsMiddleware(object):
    def __init__(self,user_agents,proxy_list,enable_proxy,redis_url):
        #取ua列表
        self.user_agents = user_agents

        # #取proxy列表
        # self.proxy_list = proxy_list
        # if self.proxy_list is None:
        #     raise KeyError('PROXY_LIST文件不存在')
        # fin = open(self.proxy_list)

        # # TODO 删除ip代理的密码
        # for line in fin.readlines():
        #     parts = re.match('(\w+:\w+@)?(.+)', line.strip())
        #     if not parts:
        #         continue
        #     # Cut trailing @
        #     if parts.group(1):
        #         user_pass = parts.group(1)[:-1]
        #     else:
        #         user_pass = ''
        #     self.proxies[parts.group(2)] = user_pass
        # fin.close()
        self.enable_proxy = enable_proxy

        self.proxies = {}
        self.server = redis.StrictRedis.from_url(redis_url)

        #phantomjs相关设置
        self.dcap = dict(DesiredCapabilities.PHANTOMJS)
        self.dcap["phantomjs.page.settings.disk-cache"] = True
        self.dcap["phantomjs.page.settings.loadImages"] = False


        # self.js = "var i=1;window.setInterval(a, 50);function a(){document.getElementsByTagName('body')[0].scrollTop=100*i;i++;}"

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENTS'],crawler.settings['PROXY_LIST'],crawler.settings['ENABLE_PROXY'],crawler.settings['REDIS_URL'])
        return o

    def process_request(self, request, spider):
        this_task_information = eval(self.server.hget('%s:task_information'%BOT_NAME,request.meta["id"]))
        if this_task_information['type'] == 1 and request.meta.has_key("this_url_rule"):#如果想对eb类网站全体用phantomjs的话，就把这个has_key去掉
            self.service_args = []
            self.service_args.append('--ignore-ssl-errors=true')  ##忽略https错误

            #找代理
            if self.enable_proxy:
                while True:
                    self.proxies = self.server.hgetall('%s:proxy_pool' % BOT_NAME)
                    del self.proxies['running']
                    if self.proxies:
                        break
                    time.sleep(1)
                self.service_args.append('--proxy=%s' % random.choice(self.proxies.keys()))
                # print self.service_args
            #随机定义ip代理、UA
            self.dcap["phantomjs.page.settings.userAgent"] = (random.choice(self.user_agents))
            # print self.dcap
            # self.dcap["phantomjs.page.customHeaders.User-Agent"] = self.dcap["phantomjs.page.settings.userAgent"]

            #开启headless浏览器并进行初始请求
            driver = webdriver.PhantomJS(service_args = self.service_args, desired_capabilities=self.dcap)
            driver.set_window_size(1500, 15000)
            # print request.url
            driver.get(request.url.replace(';','&'))
            # driver.get_screenshot_as_file(r'/root/Crawler/mycrawler/1.png')  # 测试用：打印当前
            page_source = driver.page_source.encode('utf-8')

            #本页是特殊页
            if request.meta.has_key("this_url_rule") and request.meta["this_url_rule"]:#本页是特殊页
                this_url_rule = request.meta["this_url_rule"]
                # 本页是详情页，抓取本页该抓取的商品信息、评论

                # DONE 抽取详情页的内容
                rules = this_task_information["rules"][this_url_rule]["itemcontents"]
                # print rules
                request.meta['fetcheditemcontents'] = getitemcontent(page_source, rules)

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


            driver.close()
            return HtmlResponse(request.url, status=200, body=page_source, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        if len(response.body) == 100:
            return IgnoreRequest("body length == 100")
        else:
            return response

    def get_type(self,type_num):
        if type_num == 0:
            return By.XPATH
        elif type_num == 1:
            return By.CLASS_NAME
        elif type_num == 2:
            return By.CSS_SELECTOR
        elif type_num == 3:
            return By.ID
        elif type_num == 4:
            return By.LINK_TEXT
        elif type_num == 5:
            return By.NAME
        elif type_num == 6:
            return By.TAG_NAME

    # def __del__(self):
    #     self.driver.quit()