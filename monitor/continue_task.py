# -*- coding: utf-8 -*-

import redis
from mycrawler.settings import BOT_NAME,REDIS_URL
from monitor.distributed_lock import dist_lock



def continue_task(server,id):
    with dist_lock(BOT_NAME, server):
        #查找id对应的优先级
        score = server.zscore('%s:pausing_task'%BOT_NAME, id)
        if not score:
            return False

        #从running_task中删除
        if server.zrem('%s:pausing_task'%BOT_NAME, id) != 0:
            #加入到pausing_task中
            if server.zadd('%s:running_task'%BOT_NAME, score,id) != 0:
                return True
            else:
                return False
        else:
            return False

if __name__ == '__main__':
    print continue_task(redis.StrictRedis.from_url(REDIS_URL),1)