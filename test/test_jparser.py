# -*- coding: utf-8 -*-


import urllib2
from mycrawler.util.jparser import PageModel
html = urllib2.urlopen("http://www.sohu.com/a/144736960_123753").read().decode('utf-8')
pm = PageModel(html)
result = pm.extract()

result_body_temp = ''
for x in result['content']:
    if x['type'] == 'text':
        result_body_temp += x['data']

print result_body_temp