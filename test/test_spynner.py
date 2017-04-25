#-*-coding: utf-8 -*-
import spynner

browser = spynner.Browser()
browser.show()
browser.load('www.mit.edu')
browser.wait(15)
print browser.html.encode("utf-8")
browser.close()