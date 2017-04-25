# -*- coding: utf-8 -*-


#爬虫默认需要以下settings：
#------------------------------------------------------------------------------------------------
BOT_NAME = 'mycrawler'
SPIDER_MODULES = ['mycrawler.spiders']
NEWSPIDER_MODULE = 'mycrawler.spiders'
#------------------------------------------------------------------------------------------------


#Scrapy-redis需要以下settings：
#------------------------------------------------------------------------------------------------
#爬取的调度器（默认scrapy.core.scheduler.Scheduler）
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#配置用于url去重的类（默认的过滤器基于scrapy.utils.request.request_fingerprint函数生成的请求指纹）
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 300
# }
# 请求调度使用优先队列(默认)
# SCHEDULER_PERSIST = True
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
#------------------------------------------------------------------------------------------------


#Scrapy-splash队列需要以下settings：
#------------------------------------------------------------------------------------------------
#配置消息队列所使用的过滤类
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
SPLASH_URL = 'http://192.168.28.130:8050/'
#------------------------------------------------------------------------------------------------


#USER_AGENTS池设置需要以下settings：
#------------------------------------------------------------------------------------------------
#user_agent池
USER_AGENTS=[
	"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
	"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
	"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
	"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
	"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
]
# 爬取的默认user_agent
#USER_AGENT = 'mycrawler (+http://www.yourdomain.com)'
#------------------------------------------------------------------------------------------------


#PROXY代理池设置需要以下settings：
#------------------------------------------------------------------------------------------------
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
RETRY_TIME = 3
PROXY_LIST = r'/root/Crawler/src/mycrawler/mycrawler/my_middle_wares/ippool.txt'
#------------------------------------------------------------------------------------------------


# 遵守robots.txt规则
ROBOTSTXT_OBEY = False

# 配置最大并发请求request量 (默认: 16)
#CONCURRENT_REQUESTS = 32
# 配置抓取同一个网站发出的request的延迟时间 (默认: 0)
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# 关闭cookies (默认开启)
#COOKIES_ENABLED = False

# 关闭Telnet Console(默认开启)
#TELNETCONSOLE_ENABLED = False

# 重写默认的request headers:
# 用了splash后不能用这个了
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# spider中间件
SPIDER_MIDDLEWARES = {
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,  #50 过滤出所有失败的response(返回值非200-300的)
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,  #splash的去重中间件
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,  #500 过滤出所有url不由该spider负责的request
    'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,  #700 根据生成request的response的url来设置request的referer字段
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,  #800 过滤掉url长度比urllength_limit长的request
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,  #900 用于追踪每个request在被爬取的网站的深度，用来限制爬取最大深度
}

# downloader中间件

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,  #100 过滤所有robots.txt阻止的request
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,  #300 完成使用http base auth的爬虫生成的请求认证过程
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,  #350 设置download_timeout指定的request下载超时时间，默认180s
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  #400 禁用scrapy的ua
    'mycrawler.my_middle_wares.my_user_agent_middle_ware.UserAgentMiddleWare': 400,  # !!!使用我写的ua中间件，测试无误
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,  #500 对于某些可能是由于临时问题导致失败的页面进行重试
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,  #550 设置default_request_headers指定的默认request header
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,  #580 根据meta-refresh html标签处理request重定向
    'mycrawler.my_middle_wares.my_proxy_middle_ware.RandomProxy': 581,  # !!!随机抽取ip代理
    'scrapy_splash.SplashCookiesMiddleware': 585,  # !!!splash处理cookie的中间件
    'scrapy_splash.SplashMiddleware': 586,  # !!!splash中间件
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,  #590 对gzip、deflate压缩数据的支持
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,  #600 根据response状态处理重定向的request
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,  #700 追踪了web server发送的cookie，并在之后的request中发送回去
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':750,  #750 对request设置http代理
    'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware': 830,  #830 添加对chunked transfer encoding的支持
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,  #850 保存所有通过的request、response、exception
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900  #900 为request、response提供底层缓存支持
}

# 是否开启extensions
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# 配置item pipelines
#ITEM_PIPELINES = {
#    'mycrawler.pipelines.MycrawlerPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
