# -*- coding: utf-8 -*-
import random
import re


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from ..util.press_button import press_button

from ..util.get_json_page_content import getitemcontent

class PhantomjsMiddleware(object):
    def __init__(self,user_agents,proxy_list,enable_proxy):
        #取ua列表
        self.user_agents = user_agents

        #取proxy列表
        self.proxy_list = proxy_list
        if self.proxy_list is None:
            raise KeyError('PROXY_LIST文件不存在')
        fin = open(self.proxy_list)
        self.proxies = {}
        # TODO 删除ip代理的密码
        for line in fin.readlines():
            parts = re.match('(\w+:\w+@)?(.+)', line.strip())
            if not parts:
                continue
            # Cut trailing @
            if parts.group(1):
                user_pass = parts.group(1)[:-1]
            else:
                user_pass = ''
            self.proxies[parts.group(2)] = user_pass
        fin.close()
        self.enable_proxy = enable_proxy

        #phantomjs相关设置
        self.dcap = dict(DesiredCapabilities.PHANTOMJS)
        self.dcap["phantomjs.page.settings.disk-cache"] = True
        self.dcap["phantomjs.page.settings.loadImages"] = False
        self.service_args = []
        self.service_args.append('--ignore-ssl-errors=true')  ##忽略https错误

        self.js = "var i=1;window.setInterval(a, 50);function a(){document.getElementsByTagName('body')[0].scrollTop=100*i;i++;}"

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENTS'],crawler.settings['PROXY_LIST'],crawler.settings['ENABLE_PROXY'])
        return o

    def process_request(self, request, spider):
        # {   "priority": 20,
        #     "type": 1,
        #     "rules": {
        #         "XXX": {
        #             "type": 1,
        #             "next_page_type": 0,
        #             "next_page_content": "XXX",
        #             "contents": [
        #                 {
        #                     "content_type": 0,
        #                     "content_content": "XXX"
        #                 }
        #             ]
        #         },
        #         "XXX": {
        #             "type": 0,
        #             "next_page_type": 0,
        #             "next_page_content": "XXX",
        #         }}}
        if request.meta["type"] == 1:#爬取电商网站
            #随机定义ip代理、
            self.dcap["phantomjs.page.settings.userAgent"] = (random.choice(self.user_agents))
            self.dcap["phantomjs.page.customHeaders.User-Agent"] = self.dcap["phantomjs.page.settings.userAgent"]
            if self.enable_proxy:
                self.service_args.append('--proxy=%s'%random.choice(self.proxies.keys()))
            self.driver = webdriver.PhantomJS(service_args = self.service_args, desired_capabilities=self.dcap)
            url = str(request.url)
            self.driver.set_window_size(1500, 15000)
            self.driver.get(url)
            # self.driver.get_screenshot_as_file(r'/root/Crawler/mycrawler/1.png')  # 测试用：打印当前

            if request.meta.has_key("this_url_rule") and request.meta["this_url_rule"]:#本页是特殊页
                if request.meta["rules"][request.meta["this_url_rule"]]["type"] == 1:#本页是详情页
                    # 详情页：等待评论按钮加载出来，并按下，
                    WebDriverWait(self.driver, 10, 1).until(EC.presence_of_element_located((self.get_type(request.meta["rules"][request.meta["this_url_rule"]]["comment_button_type"]),request.meta["rules"][request.meta["this_url_rule"]]["comment_button_content"])))
                    press_button(self.driver,request.meta["rules"][request.meta["this_url_rule"]]["comment_button_type"],request.meta["rules"][request.meta["this_url_rule"]]["comment_button_content"])

                # TODO 换掉这种sb的加载方式，自己算多少页

                # 抓取评论区：不断等待下一页按钮加载进来，并按下
                # try:
                #     while True:
                #         # 抓取本页内容，存入meta：
                #         # TODO 对加载进来的内容进行处理（解析、保存），写个回调函数
                #         getconmmentcontent(self.driver.page_source, request.meta["rules"][request.meta["this_url_rule"]])
                #         WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located((self.next_page_button_type,self.next_page_button_content)))
                #         press_button(self.driver,request.meta["rules"][request.meta["this_url_rule"]]["comment_button_type"],request.meta["rules"][request.meta["this_url_rule"]]["comment_button_content"])
                # except TimeoutException,e:
                #     print '%s 评论区抓取完毕'%url

                #抓取商品详情内容，抓取回来的内容加入到request,meta中去
                request.meta['fetcheditemcontents'] = getitemcontent(self.driver.page_source,request.meta["rules"][request.meta["this_url_rule"]]["itemcontents"])
            # print('网页加载完毕.....')
            self.driver.quit()
            return HtmlResponse(url, status=200, body=self.driver.page_source, encoding='utf-8', request=request)

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