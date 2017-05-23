from scrapy.utils.reqser import request_to_dict, request_from_dict
from ..settings import BOT_NAME
from scrapy_redis import picklecompat

import random

class Base(object):
    """Per-spider base queue class"""

    def __init__(self, server, spider, key, serializer=None):
        """Initialize per-spider redis queue.

        Parameters
        ----------
        server : StrictRedis
            Redis client instance.
        spider : Spider
            Scrapy spider instance.
        key: str
            Redis key where to put and get messages.
        serializer : object
            Serializer object with ``loads`` and ``dumps`` methods.

        """
        if serializer is None:
            # Backward compatibility.
            # TODO: deprecate pickle.
            serializer = picklecompat
        if not hasattr(serializer, 'loads'):
            raise TypeError("serializer does not implement 'loads' function: %r"
                            % serializer)
        if not hasattr(serializer, 'dumps'):
            raise TypeError("serializer '%s' does not implement 'dumps' function: %r"
                            % serializer)

        self.server = server
        self.spider = spider
        self.key = key % {'spider': spider.name}
        self.serializer = serializer

    def _encode_request(self, request):
        """Encode a request object"""
        obj = request_to_dict(request, self.spider)
        return self.serializer.dumps(obj)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        obj = self.serializer.loads(encoded_request)
        return request_from_dict(obj, self.spider)

    def __len__(self):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, request):
        """Push a request"""
        raise NotImplementedError

    def pop(self, timeout=0):
        """Pop a request"""
        raise NotImplementedError

    def clear(self):
        """Clear queue/stack"""
        self.server.delete(self.key)
        self.server.flushall()


class FifoQueue(Base):
    """Per-spider FIFO queue"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.llen(self.key)

    def push(self, request):
        """Push a request"""
        self.server.lpush(self.key, self._encode_request(request))

    def pop(self, timeout=0):
        """Pop a request"""
        if timeout > 0:
            data = self.server.brpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.rpop(self.key)
        if data:
            return self._decode_request(data)


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
        self.server.execute_command('ZADD', '%s:task_%s'%('mycrawler',request.meta['id']), score, data)

    def pop(self, timeout=0):
        """
        Pop a request
        timeout not support in this queue class
        """
        # use atomic range/remove using multi/exec

        # 从running_task队列中拿出一个多个优先级高的任务
        pipe = self.server.pipeline()
        pipe.multi()
        pipe.zscan('%s:running_task' % BOT_NAME)
        all_running_tasks = pipe.execute()[0][1]
        first_score = float(all_running_tasks[0][1])
        todo_tasks = []
        for i in range(len(all_running_tasks)):
            if all_running_tasks[i][1] != first_score:
                break
            else:
                todo_tasks.append(all_running_tasks[i][0])

        # 随便选择一个任务，todo_task是字符串类型
        todo_task = '%s:task_' % BOT_NAME + random.choice(todo_tasks)

        # 从task_?队列中拿出request并解码
        pipe.zrange(todo_task, 0, 0).zremrangebyrank(todo_task, 0, 0)
        results, count = pipe.execute()
        if results:
            return self._decode_request(results[0])


class LifoQueue(Base):
    """Per-spider LIFO queue."""

    def __len__(self):
        """Return the length of the stack"""
        return self.server.llen(self.key)

    def push(self, request):
        """Push a request"""
        self.server.lpush(self.key, self._encode_request(request))

    def pop(self, timeout=0):
        """Pop a request"""
        if timeout > 0:
            data = self.server.blpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.lpop(self.key)

        if data:
            return self._decode_request(data)


# TODO: Deprecate the use of these names.
SpiderQueue = FifoQueue
SpiderStack = LifoQueue
SpiderPriorityQueue = PriorityQueue
