# -*- coding: utf-8 -*-

from scrapy import Request
import redis,time
from scrapy.utils.reqser import request_to_dict, request_from_dict
from mycrawler.spiders.test_spider import test_spider
from scrapy_redis import picklecompat
from ..settings import REDIS_URL,BOT_NAME


"""
JSON格式：
{
    "XXX":{                                     #爬取目标URL
        "priority":20,                          #爬取优先级
        "type":1,                               #爬取类型，0是新闻博客，1是电商
        "rules":{                               #爬取对象的页面规则
            "XXX":{                             #页面url正则
                "type":1,                       #0是需要翻页，1是需要提取内容+翻页
                "next_page_type":0,             #下一页按钮的匹配类型，0是按xpath抓，1是按class_name抓，2是按css_selector，3是按id，4是按link_text，5是按name，6是按tag_name
                "next_page_content":"XXX",      #下一页按钮的匹配内容
                "contents":[                    #抓取内容映射关系
                    {
                        "content_type":0,       #抓取内容的匹配类型，0是按xpath抓，1是按class_name抓，2是按css_selector，3是按id，4是按link_text，5是按name，6是按tag_name
                        "content_content":"XXX" #抓取内容的匹配内容
                    }
                ]
            },
            "XXX":{   
                "type":0,  
                "next_page_type":0,
                "next_page_content":"XXX",
            }
        }
    },
    "XXXX":{  
        "priority":10,
        "type":0
    }
}
"""
start_server = redis.StrictRedis.from_url(REDIS_URL)
def add_requests(json):
    for task in json.keys():
        this_meta = json[task]
        for rule in json[task]["rules"].keys():
            if re.compile(rule).match(task):
                this_url_rule = rule
                break
        this_meta["this_url_rule"] = this_url_rule
        obj = request_to_dict(Request(task,priority = json[task]["priority"],meta = this_meta),spider = test_spider())
        obj = picklecompat.dumps(obj)
        start_server.execute_command('ZADD', '%s:start_urls'%BOT_NAME, json[task]["priority"], obj)
        # time.sleep(3)
