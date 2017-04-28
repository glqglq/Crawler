# -*- coding: utf-8 -*-


#爬虫默认需要以下settings：
#------------------------------------------------------------------------------------------------
BOT_NAME = 'mycrawler'
SPIDER_MODULES = ['mycrawler.spiders']
NEWSPIDER_MODULE = 'mycrawler.spiders'
#------------------------------------------------------------------------------------------------


#Scrapy-redis插件需要以下settings：
#------------------------------------------------------------------------------------------------
#启用Redis调度存储请求队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#确保所有的爬虫通过Redis去重（默认的过滤器基于scrapy.utils.request.request_fingerprint函数生成的请求指纹）
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 默认对请求进行序列化的程序是pickle，但是我们可以通过loads和dumps函数将其改为类似模块。注意pickle在不同python版本间是不兼容的。
# 注意：在python 3.x，序列化程序必须返回字符串键，并且支持字节作为值。由于这个原因，json或msgpack模块默认会不好用。在python2.x中没这个毛病，可以用json或msgpack来作为序列化程序。
# SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"

# 不清空redis队列，这样就可以暂停/恢复爬取
SCHEDULER_PERSIST = True

# 使用优先级调度请求队列 （默认使用）
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'

# 最大空闲时间，防止爬虫在分布式爬取时因为等待而自动关闭
# 只有queue_class是SpiderQueue或SpiderStack时才有用
# 可能在spider第一次开始爬取的同时也会阻塞（因为队列阻塞）
#SCHEDULER_IDLE_BEFORE_CLOSE = 10

# 序列化item pipeline并且作为redis key存储
REDIS_ITEMS_KEY = 'mycrawler:items'
# item序列化程序默认是ScrapyJSONEncoder。你也可以对任何可调用对象使用可导入路径。
REDIS_ITEMS_SERIALIZER = 'json.dumps'
# 如果设置此项，则此项优先级高于设置的REDIS_HOST 和 REDIS_PORT
REDIS_URL = r'redis://admin:1@192.168.28.130:6379'

# 自定义的redis客户端参数（连接超时之类的）
#REDIS_PARAMS  = {}

# 自定义redis客户端类
#REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient'

# 如果为True，程序就会就用redis的 ``spop`` 操作。如果你想在start urls中避免起始网址列表重复，就用这个。开启此选项的话urls必须通过``sadd``操作实现添加，否则你会从redis得到一个type error
#REDIS_START_URLS_AS_SET = False

# RedisSpider and RedisCrawlSpider默认的start urls键.
REDIS_START_URLS_KEY = 'mycrawler:start_urls'
#------------------------------------------------------------------------------------------------


# 配置最大并发请求request量 (默认: 16)
#CONCURRENT_REQUESTS = 32
# 配置抓取同一个网站发出的request的延迟时间 (默认: 0)
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# 关闭cookies (默认开启)
COOKIES_ENABLED = False

# 关闭Telnet Console(默认开启)
#TELNETCONSOLE_ENABLED = False


#中间件、item piplines、extensions需要设置以下settings：
#------------------------------------------------------------------------------------------------
# spider中间件
SPIDER_MIDDLEWARES = {
    #Engine side
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,  #50 过滤出所有失败的response(返回值非200-300的)
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,  #splash的去重中间件
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,  #500 过滤出所有url不由该spider负责的request
    'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,  #700 根据生成request的response的url来设置request的referer字段
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,  #800 过滤掉url长度比urllength_limit长的request
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,  #900 用于追踪每个request在被爬取的网站的深度，用来限制爬取最大深度
    # Spider side
}
# downloader中间件
DOWNLOADER_MIDDLEWARES = {
    # Engine side
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,  #100 过滤所有robots.txt阻止的request
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,  #300 完成使用http base auth的爬虫生成的请求认证过程
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,  #350 设置download_timeout指定的request下载超时时间，默认180s
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  #400 禁用scrapy的ua
    'mycrawler.my_middle_wares.my_user_agent_middle_ware.UserAgentMiddleWare': 400,  # !!!使用我写的ua中间件，测试无误
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,  #500 对于某些可能是由于临时问题导致失败的页面进行重试
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,  #550 设置default_request_headers指定的默认request header
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,  #580 根据meta-refresh html标签处理request重定向
    # 'mycrawler.my_middle_wares.my_proxy_middle_ware.RandomProxy': 581,  # !!!随机抽取ip代理
    'scrapy_splash.SplashCookiesMiddleware': 585,  # !!!splash处理cookie的中间件
    'scrapy_splash.SplashCookiesMiddleware': 585,  # !!!splash处理cookie的中间件
    'scrapy_splash.SplashMiddleware': 586,  # !!!splash中间件
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,  #590 对gzip、deflate压缩数据的支持
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,  #600 根据response状态处理重定向的request
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,  #700 追踪了web server发送的cookie，并在之后的request中发送回去
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':750,  #750 对request设置http代理
    'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware': 830,  #830 添加对chunked transfer encoding的支持
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,  #850 保存所有通过的request、response、exception
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900  #900 为request、response提供底层缓存支持
    # Downloader side
}
# 是否开启extensions：
#EXTENSIONS = {
    # 'scrapy.extensions.corestats.CoreStats': 0,
    # 'scrapy.extensions.telnet.TelnetConsole': 0,
    # 'scrapy.extensions.memusage.MemoryUsage': 0,
    # 'scrapy.extensions.memdebug.MemoryDebugger': 0,
    # 'scrapy.extensions.closespider.CloseSpider': 0,
    # 'scrapy.extensions.feedexport.FeedExporter': 0,
    # 'scrapy.extensions.logstats.LogStats': 0,
    # 'scrapy.extensions.spiderstate.SpiderState': 0,
    # 'scrapy.extensions.throttle.AutoThrottle': 0,
#}
# 配置item pipelines（默认为空）：
ITEM_PIPELINES = {

    # 'scrapy_redis.pipelines.RedisPipeline': 300,  # 将抓取项存在redis中等待方便进一步处理
    'mycrawler.my_pipelines.page_content_piplines.PageContentPipeline':400
}
#------------------------------------------------------------------------------------------------


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
# HTTPCACHE_IGNORE_MISSING = False
# HTTPCACHE_ALWAYS_STORE = False
# HTTPCACHE_IGNORE_SCHEMES = ['file']
# HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS = []
# HTTPCACHE_DBM_MODULE = 'anydbm' if six.PY2 else 'dbm'
# HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.DummyPolicy'
# HTTPCACHE_GZIP = False









#MySql数据库配置需要以下settings：
#------------------------------------------------------------------------------------------------
MYSQL_HOST = '192.168.28.130'
MYSQL_DBNAME = 'crawler'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASS = '7758521123Pp!'
#------------------------------------------------------------------------------------------------
#Scrapy-splash插件需要以下settings：
#------------------------------------------------------------------------------------------------
#配置消息队列所使用的过滤类
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
SPLASH_URL = 'http://192.168.28.130:8050/'
# 重写默认的request headers（用了splash后不能用这个了）：
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
#------------------------------------------------------------------------------------------------


#USER_AGENTS池设置需要以下settings：
#------------------------------------------------------------------------------------------------
#我写的user_agent池
USER_AGENTS=[
	"Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1"
]
# scrapy的内置user_agent设置
#USER_AGENT = 'mycrawler (+http://www.yourdomain.com)'
#------------------------------------------------------------------------------------------------

#PROXY代理池设置需要以下settings：
PROXY_LIST = r'/root/Crawler/mycrawler/my_middle_wares/ippool.txt'

# retry
#------------------------------------------------------------------------------------------------
RETRY_ENABLED = True
RETRY_HTTP_CODES = [500, 502,  503, 504, 400, 403, 404, 408]
RETRY_TIMES = 2  # initial response + 2 retries = 3 requests
# RETRY_PRIORITY_ADJUST = -1
#------------------------------------------------------------------------------------------------


# 遵守robots.txt规则
ROBOTSTXT_OBEY = False