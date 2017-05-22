from scrapy_redis import picklecompat
from mycrawler.settings import REDIS_URL
import redis

start_server = redis.StrictRedis.from_url(REDIS_URL)
pipe = start_server.pipeline()
pipe.multi()
pipe.zrange('mycrawler:requests', 0, 0).zremrangebyrank('mycrawler:requests', 0, 0)
results, count = pipe.execute()
print picklecompat.loads(results[0])