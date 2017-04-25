# -*- coding:utf-8 -*-
import urllib2
import urllib

url = 'http://www.baidu.com'
data = urllib.urlencode({'wd':'宫禄齐'})
response = urllib2.urlopen(url+'?'+data)
content = urllib2.urlopen(url+'?'+data).read()
print content