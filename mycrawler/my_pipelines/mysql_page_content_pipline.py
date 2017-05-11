# -*- coding: utf-8 -*-

from twisted.enterprise import adbapi
from scrapy import log

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class PageContentPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):

        dbargs = dict(
            host=settings['MYSQL_HOST'],
            port = settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASS'],
            charset='utf8',
            use_unicode=True,
        )
        # 使用Twisted异步数据库api，参数详见MySQLdb.connections
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self,item,spider):
        d = self.dbpool.runInteraction(self._do_sert,item,spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return item

    def _do_sert(self, conn, item, spider):
        """Perform an insert or update."""
        conn.execute("""INSERT INTO pagecontent (url, content) VALUES (%s, %s)""", (item['url'], item['content']))
        # spider.log("Item stored in db: %r" % (item))


    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)