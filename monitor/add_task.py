# -*- coding: utf-8 -*-

import redis,re

from scrapy import Request
from scrapy.utils.reqser import request_to_dict
from scrapy_redis import picklecompat
from mycrawler.settings import REDIS_URL,BOT_NAME
from monitor.distributed_lock import dist_lock



def add_task(server,json):
    """
    
    :param json:str类型，表示要添加任务的详细信息 
    :return: list，表示添加的任务ids
    """
    json = eval(json)
    ids = []

    for task in json.keys():

        #电商meta中加入this_url_rule
        this_meta = {}
        if json[task]["type"] == 1:
            this_url_rule = ''
            if json[task].has_key("rules") and json[task]["rules"]:
                for rule in json[task]["rules"].keys():
                    if re.compile(rule).match(task):
                        this_url_rule = rule
                        break
            this_meta["this_url_rule"] = this_url_rule

        json[task]["url"] = task

        with dist_lock(BOT_NAME, server):
            #获取当前任务id号
            pipe = server.pipeline()
            pipe.multi()
            pipe.zcard('%s:running_task'%BOT_NAME)
            pipe.zcard('%s:pausing_task'%BOT_NAME)
            pipe.zcard('%s:done_canceled_task'%BOT_NAME)
            id = sum(pipe.execute()) + 1
            this_meta["id"] = id

            #生成request
            req = request_to_dict(Request(task, meta=this_meta, priority=json[task]["priority"]))
            print req
            req = picklecompat.dumps(req)

            #加入到对应task_X队列(zset)、task_information队列(hash)、running_task队列(zset)
            server.execute_command('ZADD', '%s:task_%s'%(BOT_NAME,id), -json[task]["priority"], req)
            server.hset('%s:task_information'%BOT_NAME,id,json[task])
            server.zadd('%s:running_task'%BOT_NAME,-json[task]["priority"],id)
        ids.append(id)
        # time.sleep(3)
    return ids

if __name__ == '__main__':
    add_task(redis.StrictRedis.from_url(REDIS_URL),
             r'{"http://blog.sina.com.cn/":{"priority":10,"type":0,"alloweddomains":["blog.sina.com.cn"]}}')
    # add_task(redis.StrictRedis.from_url(REDIS_URL),r'{"http://www.ict.ac.cn":{"priority":10,"type":0,"alloweddomains":["ict.ac.cn","ict.cas.cn"]}}')
    # add_task(redis.StrictRedis.from_url(REDIS_URL),r'{"https://item.taobao.com/item.htm?spm=a1z09.2.0.0.GbRWO7&id=529495953918&_u=pdd68ii5c99":{"priority":20,"type":1,"alloweddomains":["taobao.com"],"rules":{".*.item.taobao.com.*":{"type":1,"itemcontents":{"XXX":{"content_type":0,"content_content":"XXX"},"XXX1":{"content_type":0,"content_content":"XXX"}}},}},}')