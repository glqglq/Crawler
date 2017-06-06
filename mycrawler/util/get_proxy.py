# -*- coding: utf-8 -*-

"""
    目前只支持单ip情况

"""
import urllib2,time,redis,httplib

from ..settings import PROXY_LIST_URL,REDIS_URL,BOT_NAME,CHANGE_PROXY_TIME,PROXY_TEST_URL,MIN_PROXY_NUM

# PROXY_LIST_URL = r'http://api.ip.data5u.com/api/get.shtml?order=8d090f91a5287eee8bd04031240892c8&num=100&area=%E4%B8%AD%E5%9B%BD&carrier=0&protocol=0&an1=1&sp1=1&sp2=2&sort=1&system=1&distinct=0&rettype=1&seprator=%0D%0A'
# REDIS_URL = r'redis://admin:1@192.168.28.134:6379'
# BOT_NAME = 'mycrawler'
# CHANGE_PROXY_TIME = 15
# PROXY_TEST_URL = r'https://amos.alicdn.com/muliuserstatus.aw?_ksTS=1495442598290_944&callback=jsonp945&beginnum=0&charset=utf-8&uids=%E6%A1%86%E5%90%89%E5%91%A81976&site=cntaobao'
# MIN_PROXY_NUM = 10
# PROXY_TEST_URL = r'http://www.ip002.net/'

start_time = time.time()

def get_proxy(server):
    """
    如果redis数据库proxy键中没有running，则不断更新代理ip到proxy键中去
    :server:redis server
    :return:空 
    """

    if not server.hget('%s:proxy_pool'%BOT_NAME, 'running') == '1':  #还没有其他的get_proxy线程
        server.hset('%s:proxy_pool'%BOT_NAME, 'running', 1)
        # 每隔三秒扫一次
        need_new = '1'
        while True:

            # 如果need_new不为空，则抓取新ip代理
            if need_new:
                while True:
                    proxy_get_opener = urllib2.build_opener()
                    try:
                        response = proxy_get_opener.open(PROXY_LIST_URL)
                        assert (response.code == 200 and response.url == PROXY_LIST_URL)
                        proxies = response.read().split()
                        assert proxies[0][0] != '{'
                        need_new = ''
                        break
                    except AssertionError,e:
                        print proxies,'频率过快'
                        time.sleep(5)
                    except Exception,e:
                        print 'NO'
                        # time.sleep(3)


                # 验证可用性，存入redis数据库
                for proxy in proxies:
                    # proxy_handler = urllib2.ProxyHandler({'http': "http://" + proxy})
                    # opener = urllib2.build_opener(proxy_handler)
                    # try:
                    #     response = opener.open(PROXY_TEST_URL)
                    #     print response.read()
                    #     assert (response.code == 200 and response.url == PROXY_TEST_URL)

                    try:
                        conn = httplib.HTTPConnection(proxy, timeout=3.0)
                        conn.request(method='GET', url=PROXY_TEST_URL, body='',
                                     headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': ''})
                        server.hset('%s:proxy_pool' % BOT_NAME,proxy,time.time())
                        # print proxy, time.time(), "可用"
                    except Exception,e:
                        pass
                        # print proxy, time.time(),"不可用"

            # 验证是否应该更换新ip：ip使用超时或者proxy_pool为空
            now_ip_proxies = server.hgetall('%s:proxy_pool' % BOT_NAME)
            for ip in now_ip_proxies.keys():
                if ip == 'running':
                    continue
                if (time.time() - float(now_ip_proxies[ip])) >= CHANGE_PROXY_TIME:
                    # print ip, time.time() - float(now_ip_proxies[ip]), time.time() - start_time
                    server.hdel('%s:proxy_pool' % BOT_NAME,ip)
                    if server.hlen('%s:proxy_pool' % BOT_NAME) <= MIN_PROXY_NUM:
                        need_new = ip


            # time.sleep(3)

if __name__ == '__main__':
    server = redis.StrictRedis.from_url(REDIS_URL)
    get_proxy(server)