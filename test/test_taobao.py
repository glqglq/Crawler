import urllib2,time
from scrapy import Selector



for i in range(50):
    try:
        ip = urllib2.urlopen(
            'http://www.taobao.com',
            timeout=3).read()
        print 'YES'
    except Exception,e:
        print "NO"

