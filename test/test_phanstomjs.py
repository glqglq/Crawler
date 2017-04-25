# from selenium import webdriver
# driver = webdriver.PhantomJS()
# driver.set_page_load_timeout(30)
# driver.get(r"https://item.jd.com/313977.html")
# data = driver.page_source
# print data
# driver.quit()

import subprocess
def getDom(url):
    cmd = r'phantomjs C:\Users\LuckyGong\Downloads\phantomjs-2.1.1-windows\bin\test_phantomjs.js'
    stdout,stderr = subprocess.Popen(cmd,shell = True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    print stderr
    return stdout
getDom(r'https://tmall.com')