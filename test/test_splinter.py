from splinter import Browser
import os

chromedriver = r"C:\Python27\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver

with Browser('chrome') as browser:
    # Visit URL
    url = "https://taobao.com"
    browser.visit(url)
    print browser.html
    browser.quit()