# -*- coding: utf-8 -*-

import re

from scrapy import Request


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

# def get_message_from_json(url,json_str):
#     meta_dict = json_str[url]
#     return Request(url,priority = json_str[url]["priority"],meta = meta_dict,dont_filter=True)

def get_message_from_response(url,response):
    this_priority = response.meta["priority"]
    this_url_rule = ''

    #识别特殊页面，设置优先级
    if response.meta["type"] == 1:#电商网站，且之前页面不是特殊页面
        for rule in response.meta["rules"].keys():
            if re.compile(rule).match(url):
                if response.meta["rules"][rule]["type"] == 1:
                    this_priority += 2
                    this_url_rule = rule
                    break
                elif response.meta["rules"][rule]["type"] == 0:
                    this_priority += 1
                    this_url_rule = rule
                    break
    clean_meta = {}
    clean_meta["priority"] = response.meta["priority"]
    clean_meta["type"] = response.meta["type"]
    if response.meta.has_key("rules"):
        clean_meta["rules"] = response.meta["rules"]
    clean_meta["this_url_rule"] = this_url_rule
    return Request(url,priority= this_priority,meta = clean_meta)