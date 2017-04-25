import requests
url = 'http://www.baidu.com'
response = requests.get(url)
content = requests.get(url).content
print "response headers:", response.headers
print "content:", content
print 'end'