# -*- coding: utf-8 -*-

import datetime

from pymongo import errors
from pymongo.mongo_client import MongoClient
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
from pymongo.read_preferences import ReadPreference

from scrapy import log
from scrapy.exporters import BaseItemExporter

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def not_set(string):
    """ Check if a string is None or ''
    :returns: bool - True if the string is empty
    """
    if string is None:
        return True
    elif string == '':
        return True
    return False


class MongoDBPipeline(BaseItemExporter):
    """ MongoDB pipeline class """
    # 默认配置
    config = {
        'uri': 'mongodb://localhost:27017',
        'fsync': False,
        'write_concern': 0,
        'database': 'scrapy-mongodb',
        'eb_collection': 'eb_items',
        'newsblog_collection': 'newsblog_items',
        'replica_set': None,
        'unique_key': None,
        'buffer': None,
        'append_timestamp': False,
        'stop_on_duplicate': 0,
    }

    # Item缓冲区
    current_eb_item = 0
    current_newsblog_item = 0
    eb_item_buffer = []
    newsblog_item_buffer = []

    # Duplicate key occurence count
    duplicate_key_count = 0

    def load_spider(self, spider):
        self.crawler = spider.crawler
        self.settings = spider.settings

        # Versions prior to 0.25
        if not hasattr(spider, 'update_settings') and hasattr(spider, 'custom_settings'):
            self.settings.setdict(spider.custom_settings or {}, priority='project')

    def open_spider(self, spider):
        self.load_spider(spider)

        # Configure the connection
        self.configure()

        if self.config['replica_set'] is not None:
            self.connection = MongoReplicaSetClient(
                self.config['uri'],
                replicaSet=self.config['replica_set'],
                w=self.config['write_concern'],
                fsync=self.config['fsync'],
                read_preference=ReadPreference.PRIMARY_PREFERRED)
        else:
            # Connecting to a stand alone MongoDB
            self.connection = MongoClient(
                self.config['uri'],
                fsync=self.config['fsync'],
                read_preference=ReadPreference.PRIMARY)

        # # Set up the collection，移入insert_item中去
        # database = connection[self.config['database']]
        # self.eb_collection = database[self.config['eb_collection']]
        # self.newsblog_collection = database[self.config['newsblog_collection']]
        # log.msg(u'Connected to MongoDB {0}, using "{1}/{2}、{3}"'.format(
        #     self.config['uri'],
        #     self.config['database'],
        #     self.config['eb_collection'],self.config['newsblog_collection']))
        #
        # # Ensure unique index
        # if self.config['unique_key']:
        #     self.eb_collection.ensure_index(self.config['unique_key'], unique=True)
        #     self.newsblog_collection.ensure_index(self.config['unique_key'], unique=True)
        #     log.msg(u'Ensuring index for key {0}'.format(
        #         self.config['unique_key']))

        # Get the duplicate on key option
        if self.config['stop_on_duplicate']:
            tmpValue = self.config['stop_on_duplicate']
            if tmpValue < 0:
                log.msg(
                    (
                        u'Negative values are not allowed for'
                        u' MONGODB_STOP_ON_DUPLICATE option.'
                    ),
                    level=log.ERROR
                )
                raise SyntaxError(
                    (
                        'Negative values are not allowed for'
                        ' MONGODB_STOP_ON_DUPLICATE option.'
                    )
                )
            self.stop_on_duplicate = self.config['stop_on_duplicate']
        else:
            self.stop_on_duplicate = 0

    def configure(self):
        """ Configure the MongoDB connection """
        # Handle deprecated configuration
        if not not_set(self.settings['MONGODB_HOST']):
            log.msg(u'DeprecationWarning: MONGODB_HOST is deprecated',level=log.WARNING)
            mongodb_host = self.settings['MONGODB_HOST']
            if not not_set(self.settings['MONGODB_PORT']):
                log.msg(u'DeprecationWarning: MONGODB_PORT is deprecated',level=log.WARNING)
                self.config['uri'] = 'mongodb://{0}:{1:i}'.format(mongodb_host,self.settings['MONGODB_PORT'])
            else:
                self.config['uri'] = 'mongodb://{0}:27017'.format(mongodb_host)

        if not not_set(self.settings['MONGODB_REPLICA_SET']):
            if not not_set(self.settings['MONGODB_REPLICA_SET_HOSTS']):
                log.msg((u'DeprecationWarning:MONGODB_REPLICA_SET_HOSTS is deprecated'),level=log.WARNING)
                self.config['uri'] = 'mongodb://{0}'.format(self.settings['MONGODB_REPLICA_SET_HOSTS'])

        # Set all regular options
        options = [
            ('uri', 'MONGODB_URI'),
            ('fsync', 'MONGODB_FSYNC'),
            ('write_concern', 'MONGODB_REPLICA_SET_W'),
            ('database', 'MONGODB_DATABASE'),
            ('eb_collection', 'MONGODB_EB_COLLECTION'),
            ('newsblog_collection', 'MONGODB_NEWSBLOG_COLLECTION'),
            ('replica_set', 'MONGODB_REPLICA_SET'),
            ('unique_key', 'MONGODB_UNIQUE_KEY'),
            ('buffer', 'MONGODB_BUFFER_DATA'),
            ('append_timestamp', 'MONGODB_ADD_TIMESTAMP'),
            ('stop_on_duplicate', 'MONGODB_STOP_ON_DUPLICATE')
        ]

        for key, setting in options:
            if not not_set(self.settings[setting]):
                self.config[key] = self.settings[setting]

        # Check for illegal configuration
        if self.config['buffer'] and self.config['unique_key']:
            log.msg(
                (
                    u'IllegalConfig: Settings both MONGODB_BUFFER_DATA '
                    u'and MONGODB_UNIQUE_KEY is not supported'
                ),
                level=log.ERROR)
            raise SyntaxError(
                (
                    u'IllegalConfig: Settings both MONGODB_BUFFER_DATA '
                    u'and MONGODB_UNIQUE_KEY is not supported'
                ))

    def process_item(self, item, spider):
        """ Process the item and add it to MongoDB
        :type item: Item object
        :param item: The item to put into MongoDB
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: Item object
        """
        item = dict(self._get_serialized_fields(item))
        # print item
        if self.config['buffer']:
            if self.config['append_timestamp']:
                item['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}

            if item['type'] == 1:#电商类
                self.current_eb_item += 1
                self.eb_item_buffer.append(item)
            else:
                self.current_newsblog_item += 1
                self.newsblog_item_buffer.append(item)




            if self.current_eb_item == self.config['buffer']:
                self.current_eb_item = 0
                return self.insert_item(self.eb_item_buffer, spider,1)
            if self.current_newsblog_item == self.config['buffer']:
                self.current_newsblog_item = 0
                return self.insert_item(self.newsblog_item_buffer, spider,0)

            else:
                return item
        if item['type'] == 1:
            return self.insert_item(self.eb_item_buffer, spider,1)
        else:
            return self.insert_item(self.newsblog_item_buffer, spider,0)

    def close_spider(self, spider):
        """ Method called when the spider is closed
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: None
        """
        if self.eb_item_buffer:
            self.insert_item(self.eb_item_buffer, spider,1)
        if self.newsblog_item_buffer:
            self.insert_item(self.newsblog_item_buffer, spider,0)

    def insert_item(self, item, spider,type):
        """ Process the item and add it to MongoDB
        :type item: (Item object) or [(Item object)]
        :param item: The item(s) to put into MongoDB
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: Item object
        """

        # Set up the collection
        database = self.connection[self.config['database']]

        if isinstance(item,list):
            for ite in item:
                ite = dict(ite)
                if self.config['append_timestamp']:
                    ite['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}

                if ite.get('type',-1) == 0:
                    self.newsblog_collection = database[self.config['newsblog_collection'] + '_' + str(ite.get('id',''))]
                    if self.config['unique_key']:
                        self.newsblog_collection.ensure_index(self.config['unique_key'], unique=True)
                    if self.config['unique_key'] is None:
                        try:
                            self.newsblog_collection.insert(ite, continue_on_error=True)
                        except errors.DuplicateKeyError:
                            if (self.stop_on_duplicate > 0):
                                self.duplicate_key_count += 1
                                if (self.duplicate_key_count >= self.stop_on_duplicate):
                                    self.crawler.engine.close_spider(
                                        spider,
                                        'Number of duplicate key insertion exceeded'
                                    )
                    else:
                        key = {}
                        if isinstance(self.config['unique_key'], list):
                            for k in dict(self.config['unique_key']).keys():
                                key[k] = ite[k]
                        else:
                            key[self.config['unique_key']] = ite[self.config['unique_key']]
                        self.newsblog_collection.update(key, ite, upsert=True)

                elif ite.get('type',-1) == 1:
                    self.eb_collection = database[self.config['eb_collection'] + '_' + str(ite.get('id')) + '_' + ite.get('this_url_rule')]
                    if self.config['unique_key']:
                        self.eb_collection.ensure_index(self.config['unique_key'], unique=True)
                    if self.config['unique_key'] is None:
                        try:
                            self.eb_collection.insert(ite, continue_on_error=True)
                        except errors.DuplicateKeyError:
                            if (self.stop_on_duplicate > 0):
                                self.duplicate_key_count += 1
                                if (self.duplicate_key_count >= self.stop_on_duplicate):
                                    self.crawler.engine.close_spider(
                                        spider,
                                        'Number of duplicate key insertion exceeded'
                                    )
                    else:
                        key = {}
                        if isinstance(self.config['unique_key'], list):
                            for k in dict(self.config['unique_key']).keys():
                                key[k] = ite[k]
                        else:
                            key[self.config['unique_key']] = ite[self.config['unique_key']]
                        self.eb_collection.update(key, ite, upsert=True)


        else:
            item = dict(item)
            if self.config['append_timestamp']:
                item['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}

            if item.get('type', -1) == 0:
                self.newsblog_collection = database[self.config['newsblog_collection'] + '_' + str(item.get('id', ''))]
                if self.config['unique_key']:
                    self.newsblog_collection.ensure_index(self.config['unique_key'], unique=True)
                if self.config['unique_key'] is None:
                    try:
                        self.newsblog_collection.insert(item, continue_on_error=True)
                    except errors.DuplicateKeyError:
                        if (self.stop_on_duplicate > 0):
                            self.duplicate_key_count += 1
                            if (self.duplicate_key_count >= self.stop_on_duplicate):
                                self.crawler.engine.close_spider(
                                    spider,
                                    'Number of duplicate key insertion exceeded'
                                )
                else:
                    key = {}
                    if isinstance(self.config['unique_key'], list):
                        for k in dict(self.config['unique_key']).keys():
                            key[k] = item[k]
                    else:
                        key[self.config['unique_key']] = item[self.config['unique_key']]
                    self.newsblog_collection.update(key, item, upsert=True)

            else:
                self.eb_collection = database[
                    self.config['eb_collection'] + '_' + str(item.get('id')) + '_' + item.get('this_url_rule')]
                if self.config['unique_key']:
                    self.eb_collection.ensure_index(self.config['unique_key'], unique=True)
                if self.config['unique_key'] is None:
                    try:
                        self.eb_collection.insert(item, continue_on_error=True)
                    except errors.DuplicateKeyError:
                        if (self.stop_on_duplicate > 0):
                            self.duplicate_key_count += 1
                            if (self.duplicate_key_count >= self.stop_on_duplicate):
                                self.crawler.engine.close_spider(
                                    spider,
                                    'Number of duplicate key insertion exceeded'
                                )
                else:
                    key = {}
                    if isinstance(self.config['unique_key'], list):
                        for k in dict(self.config['unique_key']).keys():
                            key[k] = item[k]
                    else:
                        key[self.config['unique_key']] = item[self.config['unique_key']]
                    self.eb_collection.update(key, item, upsert=True)

        self.newsblog_collection = []
        self.eb_collection = []




        # if type == 1 and  isinstance(item,list):
        #     self.eb_collection = database[self.config['eb_collection'] + '_' + str(item[0]['id']) + '_' + item[0]['this_url_rule']]
        # elif type == 0 and isinstance(item,list):
        #     self.newsblog_collection = database[self.config['newsblog_collection'] + '_' + str(item[0]['id'])]
        # elif type == 1 and not isinstance(item,list):
        #     self.eb_collection = database[
        #         self.config['eb_collection'] + '_' + str(item['id']) + '_' + item['this_url_rule']]
        # elif type == 0 and not isinstance(item,list):
        #     self.newsblog_collection = database[self.config['newsblog_collection'] + '_' + str(item['id'])]
        #
        # log.msg(u'Connected to MongoDB {0}, using "{1}/{2}、{3}"'.format(
        #     self.config['uri'],
        #     self.config['database'],
        #     self.config['eb_collection'], self.config['newsblog_collection']))
        #
        # # Ensure unique index
        # if self.config['unique_key']:
        #     self.eb_collection.ensure_index(self.config['unique_key'], unique=True)
        #     self.newsblog_collection.ensure_index(self.config['unique_key'], unique=True)
        #     log.msg(u'Ensuring index for key {0}'.format(
        #         self.config['unique_key']))
        #
        # if not isinstance(item, list):
        #     item = dict(item)
        #
        # if self.config['append_timestamp']:
        #     item['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}
        #
        # if self.config['unique_key'] is None:
        #     try:
        #         if type == 1:
        #             self.eb_collection.insert(item, continue_on_error=True)
        #             self.eb_item_buffer = []
        #             log.msg(u'Stored item(s) in MongoDB {0}/{1}'.format(self.config['database'], self.config['eb_collection']),
        #                 level=log.DEBUG,spider=spider)
        #         else:
        #             self.newsblog_collection.insert(item, continue_on_error=True)
        #             self.newsblog_item_buffer = []
        #             log.msg(u'Stored item(s) in MongoDB {0}/{1}'.format(self.config['database'],
        #                     self.config['newsblog_collection']),level=log.DEBUG, spider=spider)
        #         # print '插入成功'
        #
        #     except errors.DuplicateKeyError:
        #         log.msg(u'Duplicate key found', level=log.DEBUG)
        #         if (self.stop_on_duplicate > 0):
        #             self.duplicate_key_count += 1
        #             if (self.duplicate_key_count >= self.stop_on_duplicate):
        #                 self.crawler.engine.close_spider(
        #                     spider,
        #                     'Number of duplicate key insertion exceeded'
        #                 )
        #
        #
        # else:
        #     key = {}
        #     if isinstance(self.config['unique_key'], list):
        #         for k in dict(self.config['unique_key']).keys():
        #             key[k] = item[k]
        #     else:
        #         key[self.config['unique_key']] = item[self.config['unique_key']]
        #     if type == 1:#电商类
        #         self.eb_collection.update(key, item, upsert=True)
        #         log.msg(u'Stored item(s) in MongoDB {0}/{1}'.format(
        #             self.config['database'], self.config['eb_collection']),
        #         level=log.DEBUG,spider=spider)
        #     else:
        #         self.newsblog_collection.update(key, item, upsert=True)
        #         log.msg(u'Stored item(s) in MongoDB {0}/{1}'.format(
        #             self.config['database'], self.config['newsblog_collection']),
        #             level=log.DEBUG, spider=spider)

        return item