# -*- coding: utf-8 -*-


# 配置最大并发请求request量 (默认: 16)
CONCURRENT_REQUESTS = 32
# The maximum limit for Twisted Reactor thread pool size. This is common multi-purpose thread pool used by various Scrapy components. Threaded DNS Resolver, BlockingFeedStorage, S3FilesStore just to name a few. Increase this value if you’re experiencing problems with insufficient blocking IO.
# REACTOR_THREADPOOL_MAXSIZE = 10
# 如果启用，当从相同的网站获取数据时，Scrapy将会等待一个随机的值 (0.5到1.5之间的一个随机值 * DOWNLOAD_DELAY)。
# RANDOMIZE_DOWNLOAD_DELAY = True
# 配置抓取同一个网站发出的request的延迟时间 (默认: 0)，支持小数
# 该设定影响(默认启用的) RANDOMIZE_DOWNLOAD_DELAY 设定。 默认情况下，Scrapy在两个请求间不等待一个固定的值， 而是使用0.5到1.5之间的一个随机值 * DOWNLOAD_DELAY 的结果作为等待间隔。
# DOWNLOAD_DELAY = 3
# 对单个网站进行并发请求的最大值
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# 对单个IP进行并发请求的最大值。
# 如果非0，则忽略CONCURRENT_REQUESTS_PER_DOMAIN，使用该设定，并发限制将针对IP，而不是网站。
# 该设定也影响 DOWNLOAD_DELAY: 如果 CONCURRENT_REQUESTS_PER_IP 非0，下载延迟应用在IP而不是网站上。
# CONCURRENT_REQUESTS_PER_IP = 16
# 下载器超时时间(单位: 秒)。
DOWNLOAD_TIMEOUT = 30
#response的最大值（默认1024MB），我设置为10MB，0是无限下载
DOWNLOAD_MAXSIZE = 10737418
# The response size (in bytes) that downloader will start to warn，我设置为5MB，0是无限
DOWNLOAD_WARNSIZE = 5073741
# 关闭cookies (默认开启)
COOKIES_ENABLED = False
# 如果启用，Scrapy将记录所有在request(Cookie 请求头)发送的cookies及response接收到的cookies(Set-Cookie 接收头)。
# COOKIES_DEBUG = False
# 定义request允许重定向的最大次数，超过该限制后该request直接返回获取到的结果。默认20
REDIRECT_MAX_TIMES = 5
# 是否启用Redirect中间件。
# REDIRECT_ENABLED = True
# 有些网站使用 meta-refresh 重定向到session超时页面， 因此我们限制自动重定向到最大延迟(秒)。 =>有点不肯定:
# REDIRECT_MAX_METAREFRESH_DELAY = 100
# 修改重定向请求相对于原始请求的优先级。 负数意味着更多优先级。
# REDIRECT_PRIORITY_ADJUST = +2
# 是否启用referer中间件。
# REFERER_ENABLED = True
# 关闭Telnet Console(默认开启)
#TELNETCONSOLE_ENABLED = False
# 是否收集下载器数据
# DOWNLOADER_STATS = True
# 用于crawl的downloader.
# DOWNLOADER = 'scrapy.core.downloader.Downloader'
# 是否收集详细的深度数据。如果启用，每个深度的请求数将会被收集在数据中。
# DEPTH_STATS_VERBOSE = False
# 是否收集最大深度数据。
# DEPTH_STATS = True
# 整数值。用于根据深度调整request优先级。如果为0，则不根据深度进行优先级调整。
#  DEPTH_PRIORITY = 0
# 启用自动限速扩展。(disabled by default)
# AUTOTHROTTLE_ENABLED = False
# 初始下载延迟(单位:秒)。
# AUTOTHROTTLE_START_DELAY = 5
# 在高延迟情况下最大的下载延迟(单位秒)。
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# 起用AutoThrottle调试(debug)模式，展示每个接收到的response。 您可以通过此来查看限速参数是如何实时被调整的。
# AUTOTHROTTLE_DEBUG = False
# Meta Refresh中间件是否启用。
# METAREFRESH_ENABLED = True


# Enable and configure HTTP caching (disabled by default)
#------------------------------------------------------------------------------------------------
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
# HTTPERROR_ALLOWED_CODES
# HTTPERROR_ALLOW_ALL
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
#------------------------------------------------------------------------------------------------


# 是否启用内存调试
# MEMDEBUG_ENABLED = False
# 如果该设置不为空，当启用内存调试时将会发送一份内存报告到指定的地址；否则该报告将写到log中。
# MEMDEBUG_NOTIFY = []
# 是否启用内存使用插件。当Scrapy进程占用的内存超出限制时，该插件将会关闭Scrapy进程， 同时发送email进行通知。
# MEMUSAGE_ENABLED = False
# 在关闭Scrapy之前所允许的最大内存数(单位: MB)(如果 MEMUSAGE_ENABLED为True)。 如果为0，将不做限制。
# MEMUSAGE_LIMIT_MB = 0
# 还有很多的内存监控setting，如果想用的话去看文档
# The class that will be used for loading spiders, which must implement the SpiderLoader API.
# SPIDER_LOADER_CLASS = 'scrapy.spiderloader.SpiderLoader'
# 使用 startproject 命令创建项目时查找模板的目录。默认: scrapy模块内部的 templates
# TEMPLATES_DIR
# 收集数据的类。该类必须实现 状态收集器(Stats Collector) API.默认: 'scrapy.statscollectors.MemoryStatsCollector'
# STATS_CLASS
# 当spider结束时dump Scrapy状态数据 (到Scrapy log中)。
# STATS_DUMP = True
# spider完成爬取后发送Scrapy数据。更多内容请查看 StatsMailer 。
# STATSMAILER_RCPTS = []

# WEBSERVICE_ENABLED = True
# WEBSERVICE_HOST
# WEBSERVICE_LOGFILE
# WEBSERVICE_PORT










# 爬虫默认需要以下settings：
#------------------------------------------------------------------------------------------------
BOT_NAME = 'mycrawler'  #项目名
SPIDER_NAME = 'mycrawler'  #我自己加的，爬虫名
SPIDER_MODULES = ['mycrawler.spiders'] #Scrapy搜索spider的模块列表。
NEWSPIDER_MODULE = 'mycrawler.spiders'
TOP_LEVEL_DOMAINS = [r'.com',r'.cn',r'.co',r'.edu',r'.gov',r'.net',r'.cc',r'.me',r'.org',r'.gov',r'.cc',r'.hk',r'.tv']
#------------------------------------------------------------------------------------------------


# 中间件、item piplines、extensions需要设置以下settings：
#------------------------------------------------------------------------------------------------
# spider中间件
SPIDER_MIDDLEWARES = {
    #Engine side
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,  #50 过滤出所有失败的response(返回值非200-300的)
    # 'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,  #splash的去重中间件
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,  #500 过滤出所有url不由该spider负责的request
    'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,  #700 根据生成request的response的url来设置request的referer字段
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,  #800 过滤掉url长度比urllength_limit长的request
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,  #900 用于追踪每个request在被爬取的网站的深度，用来限制爬取最大深度
    # Spider side
}
# downloader中间件
DOWNLOADER_MIDDLEWARES = {
    # Engine side
    'mycrawler.my_middle_wares.my_phantomjs_middle_ware.PhantomjsMiddleware': 1,  # 1
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': None,  #100 过滤所有robots.txt阻止的request
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': None,  #300 完成使用http base auth的爬虫生成的请求认证过程
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,  #350 设置download_timeout指定的request下载超时时间，默认180s
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  #400 禁用scrapy的ua
    'mycrawler.my_middle_wares.my_user_agent_middle_ware.UserAgentMiddleWare': 400,  # !!!禁用我写的ua中间件，测试无误
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,  #500 对于某些可能是由于临时问题导致失败的页面进行重试
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,  #550 设置default_request_headers指定的默认request header
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,  #580 根据meta-refresh html标签处理request重定向
    # 'mycrawler.my_middle_wares.my_proxy_middle_ware.RandomProxy': 581,  # !!!随机抽取ip代理
    # 'scrapy_splash.SplashCookiesMiddleware': 585,  # !!!splash处理cookie的中间件
    # 'scrapy_splash.SplashMiddleware': 586,  # !!!splash中间件
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,  #590 对gzip、deflate压缩数据的支持
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,  #600 根据response状态处理重定向的request
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,  #700 追踪了web server发送的cookie，并在之后的request中发送回去
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':None,  #750 对request设置http代理
    'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware': 830,  #830 添加对chunked transfer encoding的支持
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,  #850 保存所有通过的request、response、exception
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,  #900 为request、response提供底层缓存支持
    # Downloader side
}
# 可用的插件列表。需要注意，有些插件需要通过设定来启用。默认情况下， 该设定包含所有稳定(stable)的内置插件。
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
# 保存项目中启用用于测试spider的scrapy contract及其顺序的字典。
# SPIDER_CONTRACTS = {
#     'scrapy.contracts.default.UrlContract': 1,
#     'scrapy.contracts.default.ReturnsContract': 2,
#     'scrapy.contracts.default.ScrapesContract': 3,
# }
# 项目中启用的下载处理器(request downloader handler)的字典。
# DOWNLOAD_HANDLERS = {
#     'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
#     'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
#     'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
#     's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
# }
# 配置item pipelines（默认为空）：
ITEM_PIPELINES = {
    # 'scrapy_redis.pipelines.RedisPipeline': 300,  # 将抓取项存在redis中等待方便进一步处理
    # 'mycrawler.my_pipelines.page_content_pipline.PageContentPipeline':100,
    'mycrawler.my_pipelines.mongodb_page_content_pipeline.MongoDBPipeline':100,
}
#------------------------------------------------------------------------------------------------

#网站总网页数量
TOTAL_PAGE = 100000000
#误判率
MISJUDGMENT_RATE = 0.000001

#Scrapy-redis插件需要以下settings：
#------------------------------------------------------------------------------------------------
#启用Redis调度存储请求队列，默认: 'scrapy.core.scheduler.Scheduler'
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#确保所有的爬虫通过Redis去重（默认的过滤器基于scrapy.utils.request.request_fingerprint函数生成的请求指纹），默认: 'scrapy.dupefilters.RFPDupeFilter'
DUPEFILTER_CLASS = "mycrawler.my_scrapy_redis_filter.dupefilter.RFPDupeFilter"
# 默认对请求进行序列化的程序是pickle，但是我们可以通过loads和dumps函数将其改为类似模块。注意pickle在不同python版本间是不兼容的。
# 注意：在python 3.x，序列化程序必须返回字符串键，并且支持字节作为值。由于这个原因，json或msgpack模块默认会不好用。在python2.x中没这个毛病，可以用json或msgpack来作为序列化程序。
# SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"
# 不清空redis队列，这样就可以暂停/恢复爬取
SCHEDULER_PERSIST = True
SCHEDULER_FLUSH_ON_START = True
# 使用优先级调度请求队列 （默认使用）
SCHEDULER_QUEUE_CLASS = 'mycrawler.my_scrapy_redis_filter.queue.SpiderPriorityQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'
# 最大空闲时间，防止爬虫在分布式爬取时因为等待而自动关闭
# 只有queue_class是SpiderQueue或SpiderStack时才有用
# 可能在spider第一次开始爬取的同时也会阻塞（因为队列阻塞）
#SCHEDULER_IDLE_BEFORE_CLOSE = 10
# 序列化item pipeline并且作为redis key存储
REDIS_ITEMS_KEY = '%s:items'%BOT_NAME
# item序列化程序默认是ScrapyJSONEncoder。你也可以对任何可调用对象使用可导入路径。
REDIS_ITEMS_SERIALIZER = 'json.dumps'
# 如果设置此项，则此项优先级高于设置的REDIS_HOST 和 REDIS_PORT
REDIS_URL = r'redis://admin:1@192.168.28.134:6379'
# 自定义的redis客户端参数（连接超时之类的）
#REDIS_PARAMS  = {}
# 自定义redis客户端类
#REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient'
# 如果为True，程序就会就用redis的 ``spop`` 操作。如果你想在start urls中避免起始网址列表重复，就用这个。开启此选项的话urls必须通过``sadd``操作实现添加，否则你会从redis得到一个type error
#REDIS_START_URLS_AS_SET = False
# RedisSpider and RedisCrawlSpider默认的start urls键.
REDIS_START_URLS_KEY = '%s:start_urls'%BOT_NAME
#分布式锁
LOCK_KEY = '%s:lock'%BOT_NAME
LOCK_TIMEOUT = 3
# REDIS_QUEUE_NAME = 'OneName'   # 如果不设置或者设置为None，则使用默认的，每个spider使用不同的去重队列和种子队列。如果设置了，则不同spider共用去重队列和种子队列

#------------------------------------------------------------------------------------------------


#Scrapy-splash插件需要以下settings：
#------------------------------------------------------------------------------------------------
#配置消息队列所使用的过滤类
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# SPLASH_URL = 'http://192.168.28.134:8050/'
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
]
# scrapy的内置user_agent设置
#USER_AGENT = 'mycrawler (+http://www.yourdomain.com)'
#------------------------------------------------------------------------------------------------

#PROXY代理池设置需要以下settings：
PROXY_LIST = r'/root/Crawler/mycrawler/my_middle_wares/ippool.txt'
ENABLE_PROXY = True
CHANGE_PROXY_TIME = 15
PROXY_LIST_URL = r'http://www.xdaili.cn/ipagent//privateProxy/getDynamicIP/DD20175256720NUOmWU/4083e822fd9511e6942200163e1a31c0?returnType=1'
PROXY_TEST_URL = r'https://amos.alicdn.com/muliuserstatus.aw?_ksTS=1495442598290_944&callback=jsonp945&beginnum=0&charset=utf-8&uids=%E6%A1%86%E5%90%89%E5%91%A81976&site=cntaobao'

# retry
#------------------------------------------------------------------------------------------------
RETRY_ENABLED = True
RETRY_HTTP_CODES = [500, 502,  503, 504, 400, 403, 404, 408]
RETRY_TIMES = 2  # initial response + 2 retries = 3 requests
# RETRY_PRIORITY_ADJUST = -1
#------------------------------------------------------------------------------------------------


# 遵守robots.txt规则
ROBOTSTXT_OBEY = False
#Compression Middleware(压缩中间件)是否开启。
COMPRESSION_ENABLED = True


#LOG相关设置
#------------------------------------------------------------------------------------------------
# LOG_ENABLED = True
# LOG_ENCODING = 'utf-8'
# LOG_FORMATTER = 'scrapy.logformatter.LogFormatter'
# LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
#stdout是否以log形式输出
# LOG_STDOUT = False
#可选的级别有: CRITICAL、 ERROR、WARNING、INFO、DEBUG。
LOG_LEVEL = 'DEBUG'
# LOG_FILE = None
# LOG_SHORT_NAMES = False
#------------------------------------------------------------------------------------------------


#MongoDB数据库配置需要以下settings：
#------------------------------------------------------------------------------------------------
MONGODB_URI = 'mongodb://192.168.28.134:27017'
MONGODB_DATABASE = 'admin'
MONGODB_NEWSBLOG_COLLECTION = 'newsblogpagecontent'
MONGODB_EB_COLLECTION = 'ebpagecontent'
MONGODB_BUFFER_DATA = 20
MONGODB_ADD_TIMESTAMP = False

# MONGODB_UNIQUE_KEY = 'url'

#If this is set to True it forces MongoDB to wait for all files to be synced before returning.
# MONGODB_FSYNC = False

# enable replica set support. 给出想要连接的replica set名。MONGODB_HOST and MONGODB_PORT should point at your config server.
# MONGODB_REPLICA_SET = 'myReplicaSetName'

# Write operations will block until they have been replicated to the specified number or tagged set of servers.
# w= always includes the replica set primary (e.g. w=3 means write to the primary and wait until replicated to two secondaries).
# Passing w=0 disables write acknowledgement and all other write concern options.
# MONGODB_REPLICA_SET_W = 0

# 置为0的话选项不起作用。置为n，当在爬行时检测到N个重复插入时，蜘蛛关闭。
# MONGODB_STOP_ON_DUPLICATE = 0
#------------------------------------------------------------------------------------------------

#MySql数据库配置需要以下settings：
#------------------------------------------------------------------------------------------------
MYSQL_HOST = '192.168.28.134'
MYSQL_DBNAME = 'crawler'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASS = '7758521123Pp!'
#------------------------------------------------------------------------------------------------

SCRAPYD_URL = '192.168.28.134'


# 弃用：
# scrapy.extensions.closespider.CloseSpider控件参数，当某些状况发生，spider会自动关闭。每种情况使用指定的关闭原因。
#------------------------------------------------------------------------------------------------
# 一个整数值，单位为秒。如果一个spider在指定的秒数后仍在运行， 它将以 closespider_timeout 的原因被自动关闭。 如果值设置为0（或者没有设置），spiders不会因为超时而关闭。
CLOSESPIDER_TIMEOUT = 0
# 一个整数值，指定条目的个数。如果spider爬取条目数超过了指定的数， 并且这些条目通过item pipeline传递，spider将会以 closespider_itemcount 的原因被自动关闭。
CLOSESPIDER_ITEMCOUNT = 0
# 一个整数值，指定最大的抓取响应(reponses)数。 如果spider抓取数超过指定的值，则会以 closespider_pagecount 的原因自动关闭。 如果设置为0（或者未设置），spiders不会因为抓取的响应数而关闭。
CLOSESPIDER_PAGECOUNT = 0
# 一个整数值，指定spider可以接受的最大错误数。 如果spider生成多于该数目的错误，它将以 closespider_errorcount 的原因关闭。 如果设置为0（或者未设置），spiders不会因为发生错误过多而关闭。
CLOSESPIDER_ERRORCOUNT = 0
#------------------------------------------------------------------------------------------------