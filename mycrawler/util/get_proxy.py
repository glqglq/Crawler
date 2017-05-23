# -*- coding: utf-8 -*-

"""
    目前只支持单ip情况

"""
import urllib2,time,redis

from ..settings import PROXY_LIST_URL,REDIS_URL,BOT_NAME,CHANGE_PROXY_TIME,PROXY_TEST_URL

# PROXY_LIST_URL = r'http://www.xdaili.cn/ipagent/privateProxy/getDynamicIP/DD20175228809744WXT/5b1e075c0a2c11e7a12d00163e1a31c0?returnType=1'
# REDIS_URL = r'redis://admin:1@192.168.28.134:6379'
# BOT_NAME = 'mycrawler'
# CHANGE_PROXY_TIME = 15


start_time = time.time()

def get_proxy():
    server = redis.StrictRedis.from_url(REDIS_URL)
    if not server.hget('%s:proxy_pool'%BOT_NAME, 'running') == '1':
        server.hset('%s:proxy_pool'%BOT_NAME, 'running', 1)
        # 每隔三秒扫一次
        need_new = '1'
        while True:

            # 如果need_new不为空，则抓取新ip代理
            if need_new:
                while True:
                    try:
                        opener = urllib2.build_opener()
                        urllib2.install_opener(opener)
                        proxies = urllib2.urlopen(PROXY_LIST_URL).read().split()
                        assert proxies[0][0] != '{'
                        break
                    except AssertionError,e:
                        print '频率过快'
                        time.sleep(5)
                    except Exception,e:
                        print 'NO'
                        # time.sleep(3)


                # 验证可用性，存入redis数据库
                for proxy in proxies:
                    try:
                        proxy_handler = urllib2.ProxyHandler({'http': "http://" + proxy})
                        opener = urllib2.build_opener(proxy_handler)
                        urllib2.install_opener(opener)
                        urllib2.urlopen(PROXY_TEST_URL)
                        server.hset('%s:proxy_pool' % BOT_NAME,proxy,time.time())
                        server.hdel('%s:proxy_pool' % BOT_NAME, need_new)
                        need_new = ''
                    except:
                        print "NO!!!!!!"

            # 验证是否应该更换新ip：ip使用超时或者proxy_pool为空
            now_ip_proxies = server.hgetall('%s:proxy_pool' % BOT_NAME)
            for ip in now_ip_proxies.keys():
                if ip == 'running':
                    continue
                if (time.time() - float(now_ip_proxies[ip])) >= CHANGE_PROXY_TIME:
                    print ip, time.time() - float(now_ip_proxies[ip]), time.time() - start_time
                    need_new = ip


            # time.sleep(3)

if __name__ == '__main__':
    get_proxy()