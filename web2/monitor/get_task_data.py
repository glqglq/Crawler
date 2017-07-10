# -*- coding: utf-8 -*-

import pymongo

from bson.objectid import ObjectId
from settings import MONGODB_NEWSBLOG_COLLECTION

client = pymongo.MongoClient('localhost', 27017)
db = client['admin']
def get_eb_task_data(id,re_rule,start,end):
    """

    :param url:
    :param start:
    :param end:
    :return:
    """
    collection = db[MONGODB_NEWSBLOG_COLLECTION + '_' + str(id) + '_' + re_rule]
    index = collection.find( { "$and": [ { "_id": { "$gte":  collection.find()[start]["_id"]} }, { "_id": { "$lt":  collection.find()[end + 1]["_id"]} } ] })
    results = []
    for item in index:
        results.append(item)
    return results

def get_newsblog_task_data(id,start,end):
    """
    传入任务id、开始下标、结束下标
    返回从mongoDB中得到的对应下标的item
    :param id:
    :param start:
    :param end:
    :return:
    """
    collection = db[MONGODB_NEWSBLOG_COLLECTION + '_' + str(id)]
    index = collection.find( { "$and": [ { "_id": { "$gte":  collection.find()[start]["_id"]} }, { "_id": { "$lt":  collection.find()[end + 1]["_id"]} } ] })
    results = []
    for item in index:
        results.append(item)
    return results