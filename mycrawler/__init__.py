# from twisted.internet import reactor,defer
# from scrapy.crawler import CrawlerProcess,CrawlerRunner
# from scrapy.cmdline import execute
# from spiders.test_spider import test_spider
#
# execute()
#
# process = CrawlerProcess()
# process.crawl(test_spider)
# process.crawl(test_spider)
# process.start() # the script will block here until the crawling is finished
#
#
# runner = CrawlerRunner()
# runner.crawl(test_spider)
# runner.crawl(test_spider)
# d = runner.join()
# d.addBoth(lambda _: reactor.stop())
# reactor.run()
#
#
# runner = CrawlerRunner()
# @defer.inlineCallbacks
# def crawl():
# 	yield runner.crawl(test_spider)
# 	yield runner.crawl(test_spider)
# 	reactor.stop()
# crawl()
# reactor.run() # the script will block here until the last crawl call is finished
#
#
#
#
#
# from scrapy.commands import ScrapyCommand
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.conf import arglist_to_dict
#
# class Command(ScrapyCommand):
# 	requires_project = True
# 	def syntax(self):
# 		return '[options]'
# 	def short_desc(self):
# 		return 'Runs all of the spiders'
# 	def add_options(self, parser):
# 		ScrapyCommand.add_options(self, parser)
# 		parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
# 						  help="set spider argument (may be repeated)")
# 		parser.add_option("-o", "--output", metavar="FILE",
# 						  help="dump scraped items into FILE (use - for stdout)")
# 		parser.add_option("-t", "--output-format", metavar="FORMAT",
# 						  help="format to use for dumping items with -o")
# 	def process_options(self, args, opts):
# 		ScrapyCommand.process_options(self, args, opts)
# 		try:
# 			opts.spargs = arglist_to_dict(opts.spargs)
# 		except ValueError:
# 			raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
# 	def run(self, args, opts):
# 		#settings = get_project_settings()
#
# 		spider_loader = self.crawler_process.spider_loader
# 		for spidername in args or spider_loader.list():
# 			print "*********cralall spidername************" + spidername
# 			self.crawler_process.crawl(spidername, **opts.spargs)
# 		self.crawler_process.start()