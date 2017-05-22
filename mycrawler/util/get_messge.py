# -*- coding: utf-8 -*-

import re

from scrapy import Request


"""
JSON格式：
{
    "XXX":{                                     #爬取目标URL
        "priority":20,                          #爬取优先级
        "type":1,                               #爬取类型，0是新闻博客，1是电商
        "alloweddomains":["XXX"],               #允许的域名
        "rules":{                               #爬取对象的页面规则
            "XXX":{                             #页面url正则
                "comment_button_type":0,        #评论按钮的匹配类型
                "comment_button_content":"XXX", #评论按钮的匹配内容
                "next_page_type":0,             #下一页按钮的匹配类型，0是按xpath抓，1是按class_name抓，2是按css_selector，3是按id，4是按link_text，5是按name，6是按tag_name
                "next_page_content":"XXX",      #下一页按钮的匹配内容
                "itemcontents":[                    #抓取内容映射关系
                    "XXX":{
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
    if response.meta["type"] == 1:
        electronic_business_get_message_from_response(url,response)
    else:
        news_blogs_get_message_from_response(url,response)

def news_blogs_get_message_from_response(url,response):
    return Request(url, priority=response.meta["priority"], meta=response.meta)



def electronic_business_get_message_from_response(url,response):
    #meta中的riority是永远不变的
    this_url_priority = response.meta["priority"]
    this_url_rule = ''

    #识别特殊页面，设置优先级和
    if response.meta.has_key("rules") and response.meta["rules"]:
        for rule in response.meta["rules"].keys():
            if re.compile(rule).match(url):
                this_url_rule = rule
                # 详情页，优先级增加
                this_url_priority += 1

    #meta中共五项：priority、type、alloweddomains、this_url_rule、rules
    clean_meta = response.meta
    clean_meta["this_url_rule"] = this_url_rule
    return Request(url,priority= this_url_priority,meta = clean_meta)