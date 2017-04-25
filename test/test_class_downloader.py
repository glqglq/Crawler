import random,urlparse,urllib2
from test_urllib2 import Throttle

class Downloader:
    def __init__(self,delay = 5,user_agent = 'wswp',proxies = None,num_retries = 1,cache = None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except:
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    result = None
        if result is None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent':self.user_agent}
            result = self.download(url,headers,proxy,self.num_retries)
            if self.cache:
                self.cache[url] = result
            return result['html']
    def download(self,url,headers,proxy,num_retries,data = None):
        request = urllib2.Request(url, headers=headers)
        opener = urllib2.build_opener()
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            html = opener.open(request).read()
        except urllib2.HTTPError, e:
            print e.reason
            html = None
            if num_retries < 2 and hasattr(e, 'code') and 500 <= e.code < 600:
                return self.download(url, num_retries=num_retries + 1)
        return html