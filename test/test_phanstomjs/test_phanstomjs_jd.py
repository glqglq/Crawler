# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from mycrawler.settings import USER_AGENTS

import time,random,redis


#设置优化属性
service_args=[]
# service_args.append('--load-images=no')  ##关闭图片加载
service_args.append('--disk-cache=yes')  ##开启缓存
service_args.append('--ignore-ssl-errors=true') ##忽略https错误


dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.disk-cache"] = True
dcap["phantomjs.page.settings.loadImages"] = False
dcap["phantomjs.page.settings.userAgent"] = random.choice(USER_AGENTS)

server = redis.StrictRedis.from_url(r'redis://admin:1@192.168.28.134:6379')
print dcap
print service_args
# while True:
#     proxies = server.hgetall('mycrawler:proxy_pool')
#     del proxies['running']
#     if proxies:
#         break
#     time.sleep(1)

service_args.append('--proxy=%s' % '93.190.23.83:8080')
loadjs = "var i=1;window.setInterval(a, 50);function a(){document.getElementsByTagName('body')[0].scrollTop=100*i;i++;}"
print time.ctime()
driver = webdriver.PhantomJS(service_args=service_args,desired_capabilities=dcap)
driver.set_window_size(1500, 15000)
print time.ctime()
driver.get(r'http://www.ip002.net/')
print driver.page_source
# WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.XPATH,r'//*[@id="J_TabBar"]/li[2]/a')))
# elem = driver.find_element_by_xpath(r'//*[@id="J_TabBar"]/li[2]/a').click()
# print time.ctime()
# driver.execute_script(loadjs)
# WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH,r'//*[@id="review-308263590694"]')))
# elem1 = driver.find_element_by_xpath(r'//*[@id="review-308263590694"]').click()
print time.ctime()
data = driver.page_source
driver.get_screenshot_as_file('1.png')
# print data
driver.close()
driver.quit()
