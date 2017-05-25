# -*- coding: utf-8 -*-

import random,time

from scrapy_redis.queue import Base
from ..settings import BOT_NAME

class PriorityQueue(Base):
    """Per-spider priority queue abstraction using redis' sorted set"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.zcard(self.key)

    def push(self, request):
        """Push a request"""
        data = self._encode_request(request)
        score = -request.priority
        # We don't use zadd method as the order of arguments change depending on
        # whether the class is Redis or StrictRedis, and the option of using
        # kwargs only accepts strings, not bytes.
        self.server.execute_command('ZADD', '%s:task_%s'%(BOT_NAME,request.meta['id']), score, data)

    def pop(self, timeout=0):
        """
        Pop a request
        timeout not support in this queue class
        """
        # use atomic range/remove using multi/exec

        # 从running_task队列中拿出一个或多个优先级高的任务
        while 1:
            pipe = self.server.pipeline()
            pipe.multi()
            pipe.zscan('%s:running_task' % BOT_NAME)
            try:
                all_running_tasks = pipe.execute()[0][1]

                first_score = float(all_running_tasks[0][1])
                todo_tasks = []
                for i in range(len(all_running_tasks)):
                    if all_running_tasks[i][1] != first_score:
                        break
                    else:
                        todo_tasks.append(all_running_tasks[i][0])
                break
            except Exception,e:
                time.sleep(2)

        # 随便选择一个任务，todo_task是字符串类型
        todo_task = '%s:task_' % BOT_NAME + random.choice(todo_tasks)

        # 从task_?队列中拿出request并解码
        pipe.zrange(todo_task, 0, 0).zremrangebyrank(todo_task, 0, 0)
        results, count = pipe.execute()
        if results:
            return self._decode_request(results[0])



# TODO: Deprecate the use of these names.
SpiderPriorityQueue = PriorityQueue
