# -*- coding: utf-8 -*-
import redis

from mycrawler.settings import REDIS_URL,BOT_NAME
from monitor.distributed_lock import dist_lock

def list_task(server):
    with dist_lock(BOT_NAME, server):
        all_task_information = server.hgetall('%s:task_information'%BOT_NAME)  #返回dict类型，键值都是str类型
        all_task_information_eval = {}
        for task_information_id in all_task_information:
            task_information_eval = eval(all_task_information[task_information_id])

            if server.zscore('%s:running_task'%BOT_NAME,task_information_id):
                task_information_eval['status'] = 1  #正在跑
            elif server.zscore('%s:pausing_task'%BOT_NAME,task_information_id):
                task_information_eval['status'] = 2  #暂停
            elif server.zscore('%s:done_canceled_task'%BOT_NAME,task_information_id):
                task_information_eval['status'] = 3  #取消或完成

            all_task_information_eval[task_information_id] = task_information_eval

    return all_task_information_eval

if __name__ == '__main__':
    print list_task(redis.StrictRedis.from_url(REDIS_URL))