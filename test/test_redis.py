# -*- coding: utf-8 -*-

from redis import client
from mycrawler.settings import REDIS_URL

server = client.StrictRedis().from_url(REDIS_URL)
pipe = server.pipeline()
pipe.multi()
pipe.zrange('hehe', 0, 0).zremrangebyrank('hehe', 0, 0)
results, count = pipe.execute()
print results[0]