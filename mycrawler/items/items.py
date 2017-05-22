# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader

class MyCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    type = scrapy.Field()
    content = scrapy.Field()


# class MyCrawlerItem(ItemLoader):
#     default_item_class = MyCrawlerItem()

