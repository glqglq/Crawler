# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time


#设置优化属性
service_args=[]
service_args.append('--load-images=no')  ##关闭图片加载
service_args.append('--disk-cache=yes')  ##开启缓存
service_args.append('--ignore-ssl-errors=true') ##忽略https错误
loadjs = "var i=1;window.setInterval(a, 50);function a(){document.getElementsByTagName('body')[0].scrollTop=100*i;i++;}"
print time.ctime()
driver = webdriver.PhantomJS(service_args=service_args)
driver.set_window_size(1500, 15000)
print time.ctime()
driver.get(u'https://item.taobao.com/item.htm?spm=a230r.1.14.11.hAKZ5j&id=541911331991&ns=1&abbucket=6&wwlight=cntaobao%E6%A1%86%E5%90%89%E5%91%A81976-%7B541911331991%7D#detail')
WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.XPATH,r'//*[@id="J_TabBar"]/li[2]/a')))
elem = driver.find_element_by_xpath(r'//*[@id="J_TabBar"]/li[2]/a').click()
print time.ctime()
driver.execute_script(loadjs)
WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH,r'//*[@id="review-308263590694"]')))
elem1 = driver.find_element_by_xpath(r'//*[@id="review-308263590694"]').click()
print time.ctime()
data = driver.page_source
driver.get_screenshot_as_file('1.png')
# print data
driver.close()
driver.quit()
