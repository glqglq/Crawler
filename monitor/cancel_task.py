# -*- coding: utf-8 -*-

import redis,time
from mycrawler.settings import BOT_NAME,REDIS_URL
from monitor.distributed_lock import dist_lock


def cancel_task(server,id):
    with dist_lock(BOT_NAME, server):
        # 查score
        score = server.zscore('%s:running_task'%BOT_NAME, id)
        if not score:
            score = server.zscore('%s:pausing_task' % BOT_NAME, id)
        if not score:
            return False

        #从running_task中删除
        if server.zrem('%s:running_task'%BOT_NAME, id) != 0:
            #加入到done_canceled_task中
            if server.zadd('%s:done_canceled_task'%BOT_NAME, score,id) != 0:
                #删除对应的task队列
                time.sleep(2)
                if server.delete('%s:task_%s'%(BOT_NAME,id)):
                    return True
                else:
                    return False
            else:
                return False
        # 从pausing_task中删除
        elif server.zrem('%s:pausing_task'%BOT_NAME, id) != 0:
            #加入到done_canceled_task中
            if server.zadd('%s:done_canceled_task'%BOT_NAME, score,id) != 0:
                # 删除对应的task队列
                time.sleep(2)
                if server.delete('%s:task_%s'%(BOT_NAME,id)):
                    return True
                else:
                    return False
            else:
                return False
        #两个队列中都未发现，停止失败
        else:
            return False

if __name__ == '__main__':
    # cancel_task(redis.StrictRedis.from_url(REDIS_URL),2)
    cancel_task(redis.StrictRedis.from_url(REDIS_URL),1)