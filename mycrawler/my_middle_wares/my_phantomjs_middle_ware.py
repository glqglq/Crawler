# -*- coding: utf-8 -*-
import random
import re


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse, Response
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException


class PhantomjsMiddleware(object):
    def __init__(self,user_agents,proxy_list,enable_proxy,enable_js):
        #取ua列表
        self.user_agents = user_agents
        self.enable_js = enable_js

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

        #翻页的相关配置
        self.button_get_type = By.XPATH
        self.button_get_content = r'//*[@id="detail"]/div[1]/ul/li[5]'
        self.next_page_button_type = By.CLASS_NAME
        self.next_page_button_content = r'ui-pager-next'
        # self.total_page =

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENTS'],crawler.settings['PROXY_LIST'],crawler.settings['ENABLE_PROXY'],crawler.settings['ENABLE_JS'])
        return o

    def process_request(self, request, spider):
        if self.enable_js:
            #随机定义ip代理、
            self.dcap["phantomjs.page.settings.userAgent"] = (random.choice(self.user_agents))
            self.dcap["phantomjs.page.customHeaders.User-Agent"] = self.dcap["phantomjs.page.settings.userAgent"]
            if self.enable_proxy:
                print '开启设置代理ip'
                self.service_args.append('--proxy=%s'%random.choice(self.proxies.keys()))
            self.driver = webdriver.PhantomJS(service_args = self.service_args, desired_capabilities=self.dcap)
            url = str(request.url)
            self.driver.set_window_size(1500, 15000)
            print '正在加载网站-%s' % url
            self.driver.get(url)
            # 测试用：打印当前
            # self.driver.get_screenshot_as_file(r'/root/Crawler/mycrawler/1.png')

            # 等待评论按钮加载出来，并按下
            WebDriverWait(self.driver, 10, 1).until(EC.presence_of_element_located((self.button_get_type,self.button_get_content)))
            self.press_button(self.button_get_type,self.button_get_content)
            # self.driver.execute_script(self.js)

            # 不断等待下一页按钮加载进来，并按下
            try:
                # TODO 换掉这种sb的加载方式，自己算多少页
                while True:
                    WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located((self.next_page_button_type,self.next_page_button_content)))
                    # TODO 对加载进来的内容进行处理（解析、保存），写个回调函数
                    self.press_button(self.next_page_button_type,self.button_get_content)
            except TimeoutException,e:
                print '%s 评论区抓取完毕'%url

            content = self.driver.page_source.encode('utf-8')
            print('网页加载完毕.....')
            self.driver.quit()
            return HtmlResponse(url, status=200, body=content, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        if len(response.body) == 100:
            return IgnoreRequest("body length == 100")
        else:
            return response

    def press_button(self,button_get_type,button_get_content):
        if button_get_type is By.XPATH:
            self.driver.find_element_by_xpath(button_get_content).click()
        elif button_get_type is By.CLASS_NAME:
            self.driver.find_element_by_class_name(button_get_content).click()
        elif button_get_type is By.CSS_SELECTOR:
            self.driver.find_element_by_css_selector(button_get_content).click()
        elif button_get_type is By.ID:
            self.driver.find_element_by_id(button_get_content).click()
        elif button_get_type is By.LINK_TEXT:
            self.driver.find_element_by_link_text(button_get_content).click()
        elif button_get_type is By.NAME:
            self.driver.find_element_by_name(button_get_content).click()
        elif button_get_type is By.TAG_NAME:
            self.driver.find_element_by_tag_name(button_get_content).click()

    # def __del__(self):
    #     self.driver.quit()