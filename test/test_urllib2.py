# -*- coding:utf-8 -*-
import urllib2,re,urlparse,datetime,time
web_url = 'http://www.baidu.com'
user_agent = 'BaiduCrawler'
max_try = 2

class Throttle(object):
    def __init__(self,delay):
        self.delay = delay  #
        self.domains = {}

    def wait(self,url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs =self.delay - (datetime.datatime.noe() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.datetime.now()

def download(url,user_agent =  'wswp',proxy = None,now = 1):
    headers = {'User-agent':user_agent}
    request = urllib2.Request(url,headers = headers)
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
    except urllib2.HTTPError,e:
        print e.reason
        html = None
        if now < 2 and hasattr(e,'code') and 500 <= e.code < 600:
            return  download(url,now = now + 1)
    return  html

def get_links(url):
    sitemap = download(url)
    links = re.findall(r'<loc>(.*?)</loc>',sitemap)
    return links

def link_crawler(seed_url,link_regex):
    import re
    crawler_queue = [seed_url]
    seen = {}
    while crawler_queue:
        url = crawler_queue.pop()
        html = download(url,now = 1)
        from robotparser import RobotFileParser
        rp = RobotFileParser().set_url(web_url.join('robots.txt')).read()
        for link in get_links(url):
            depth = seen.get(link,1)
            seen[link] = depth
            if re.match(link_regex,link) and link not in seen and rp.can_fetch(user_agent,web_url) and seen[link] != max_try:
                seen[link] = depth + 1
                link = urlparse.urljoin(seed_url,link)
                crawler_queue.append(link)

if __name__ == '__main__':
    #print download("http://www.meetup.com",'wswp',1)
    #crawel_sitemap("http://www.oschina.net/sitemap.xml")
    pass