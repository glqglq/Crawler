# -*- coding: utf-8 -*-

import redis,re


from scrapy import Request
from scrapy.utils.reqser import request_to_dict
from scrapy_redis import picklecompat
from settings import REDIS_URL,BOT_NAME
from distributed_lock import dist_lock



def add_task(server,json):
    """
    
    :param json:dict类型，表示要添加任务的详细信息
    :return: list，表示添加的任务ids
    """
    ids = []
    with dist_lock(BOT_NAME, server):
        #电商meta中加入this_url_rule
        this_meta = {}
        if json.get("type",None) == 1:
            this_url_rule = ''
            if json.get("rules",None):
                for rule in json["rules"].keys():
                    if re.compile(rule).match(json.get('url'),None):
                        this_url_rule = rule
                        break
            this_meta["this_url_rule"] = this_url_rule

        #获取当前任务id号
        pipe = server.pipeline()
        pipe.multi()
        pipe.zcard('%s:running_task'%BOT_NAME)
        pipe.zcard('%s:pausing_task'%BOT_NAME)
        pipe.zcard('%s:done_canceled_task'%BOT_NAME)
        id = sum(pipe.execute()) + 1
        this_meta["id"] = id

        # print id,this_meta,json

        #生成request
        req = request_to_dict(Request(json['url'], meta=this_meta, priority=json["priority"]))
        req = picklecompat.dumps(req)

        #加入到对应task_X队列(zset)、task_information队列(hash)、running_task队列(zset)
        server.execute_command('ZADD', '%s:task_%s'%(BOT_NAME,id), -json["priority"], req)
        server.hset('%s:task_information'%BOT_NAME,id,json)
        server.zadd('%s:running_task'%BOT_NAME,-json["priority"],id)
        ids.append(id)
        # time.sleep(3)
    return ids

if __name__ == '__main__':
    # add_task(redis.StrictRedis.from_url(REDIS_URL),
    #          r'{"http://blog.sina.com.cn/":{"priority":10,"type":0,"alloweddomains":["blog.sina.com.cn"]}}')
    add_task(redis.StrictRedis.from_url(REDIS_URL),eval(r'{"url":"http://www.ict.ac.cn","priority":10,"type":0,"alloweddomains":["ict.ac.cn","ict.cas.cn"]}'))
    # add_task(redis.StrictRedis.from_url(REDIS_URL),r'{"http://taobao.com":{"priority":20,"type":1,"alloweddomains":["taobao.com"],"rules":{".*.item.taobao.com.*":{"type":0,"itemcontents":{"name":{"content_type":1,"content_content":"tb-main-title"},"price":{"content_type":1,"content_content":"tb-rmb-num"},"place":{"content_type":3,"content_content":"J-From"},"renqi":{"content_type":1,"content_content":"J_FavCount"},"coments":{"content_type":3,"content_content":"J_RateCounter"},"jiaoyiliang":{"content_type":3,"content_content":"J_SellCounter"}}}}}}')