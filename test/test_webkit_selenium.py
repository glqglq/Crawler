from selenium import webdriver
import os,time

from selenium import webdriver
# chromedriver = r"C:\Python27\chromedriver.exe"
# os.environ["webdriver.chrome.driver"] = chromedriver
# firefox = r"C:\Python27\geckodriver.exe"
# os.environ["webdriver.firefox.driver"] = firefox


driver = webdriver.Chrome(r'C:\Python27\chromedriver.exe')
driver.get(u'https://taobao.com')
driver.maximize_window()
# driver.implicitly_wait(30)
print driver.page_source

driver.quit()
