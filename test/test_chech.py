import urllib2,time

def check(proxy):
    start = time.time()
    url = "http://amos.alicdn.com/muliuserstatus.aw?_ksTS=1495442598290_944&callback=jsonp945&beginnum=0&charset=utf-8&uids=%E6%A1%86%E5%90%89%E5%91%A81976&site=cntaobao"
    proxy_handler = urllib2.ProxyHandler({'http': "http://" + proxy})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
    # req = urllib2.Request(url)

    try:
        response = urllib2.urlopen(url, timeout = 3).read()
        # if response.code == 200 and response.url == url:
        print 'OK',proxy,time.time() - start
        # print Selector(text = response).xpath(r'/html/body/div[1]/div[2]/div[2]/div/div[2]/text()').extract()[0].strip()

        # print response
        # else:
        #     print "NO"
    except Exception:
        response = None
        print "NO",proxy,time.time() - start



# ips = ips.split()

ips = """
123.53.134.106:38559
180.122.150.111:21297
125.109.192.137:44530
140.250.132.58:47897
222.85.39.52:33977
123.53.136.114:23173
27.154.144.99:24282
115.221.117.34:43830
117.90.108.55:35299
114.239.145.53:29480
123.53.137.37:45020
121.207.69.62:26353
121.232.198.32:29694
180.104.72.11:29731
180.122.156.207:37752
144.255.49.253:25249
175.147.100.112:26315
122.241.219.5:22418
121.226.170.118:49915
117.90.52.18:36203
"""
# print ips
ips = ips.split()
for ip in ips:
    check(ip)
# s = time.time()
# while True:
#     # try:
#     #     start = time.time()
#     #     opener = urllib2.build_opener()
#     #     urllib2.install_opener(opener)
#     #     proxy = urllib2.urlopen(r'http://www.xdaili.cn/ipagent/newExclusive/getIp?spiderId=c352f3e078a14cb7b10b6ec82f60917b&orderno=MF20175228883hTv0Nw&returnType=1&count=1').read().split()[0]
#     # except Exception,e:
#     #     print proxy
#     # print time.time() - s,proxy,time.time() - start,
#     proxy = ''
#     check(proxy)
#     # time.sleep(15)