# -*- coding: utf-8 -*-


# redis数据结构
# -------------------------------------------------------------------
# 1.dupefilterX：去重-stringbit
# 2.running_task：正在运行的任务—zset(id priority)
# 3.pausing_task：暂停的任务-zset(id priority)
# 4.done_canceled_task：已完成、取消的任务-zset(id priority)
# 5.task_X：X号任务的request队列-zset(request-priority)
# 6.task_information：所有任务的信息-hash(id-json)
# -------------------------------------------------------------------



#add_task时的json
a = """
{
    "XXX":{                                     #爬取目标URL
        "priority":20,                          #爬取优先级
        "type":1,                               #爬取类型，0是新闻博客，1是电商
        "alloweddomains":["XXX"],               #允许的domains
        "rules":{                               #爬取对象的页面规则
            "XXX":{                             #页面url正则
                "type":1,                       #0是需要翻页，1是需要提取内容+翻页
                "comment_button_type":0,        #评论按钮类型
                "comment_button_content":"XXX", #评论按钮内容
                "next_page_type":0,             #下一页按钮的匹配类型，0是按xpath抓，1是按class_name抓，2是按css_selector，3是按id，4是按link_text，5是按name，6是按tag_name
                "next_page_content":"XXX",      #下一页按钮的匹配内容
                "itemcontents":{                #抓取内容映射关系
                    "XXX":{                     #抓取内容的key，对应存到mongodb数据库的key
                        "content_type":0,       #抓取内容的匹配类型，0是按xpath抓，1是按class_name抓，2是按css_selector，3是按id，4是按link_text，5是按name，6是按tag_name
                        "content_content":"XXX" #抓取内容的匹配内容
                    },
                    "XXX":{
                        "content_type":0,
                        "content_content":"XXX"
                    }
                }
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


# task_information中的json
b ="""
{
    "1":{
        "url":"XXX",
        "priority":20,
        "type":1,
        "alloweddomains":["XXX"],
        "rules":{
            "XXX":{   
                "type":1,  
                "comment_button_type":0,
                "comment_button_content":"XXX",
                "next_page_type":0,
                "next_page_content":"XXX",
                "itemcontents":{
                    "XXX":{
                        "content_type":0,
                        "content_content":"XXX"
                    }
                }
            },
            "XXX":{   
                "type":0,  
                "next_page_type":0,
                "next_page_content":"XXX",
            }
        }
    }
}
"""

# list_task返回的json
c = """
{
    "1":{
        "url":"XXX",
        "priority":20,
        "type":1,
        "status":1,
        "alloweddomains":["XXX"],
        "rules":{
            "XXX":{   
                "type":1,  
                "comment_button_type":0,
                "comment_button_content":"XXX",
                "next_page_type":0,
                "next_page_content":"XXX",
                "itemcontents":{
                    "XXX":{
                        "content_type":0,
                        "content_content":"XXX"
                    }
                }
            },
            "XXX":{   
                "type":0,  
                "next_page_type":0,
                "next_page_content":"XXX",
            }
        }
    }
}
"""

eb_meta = """
{
	"this_url_rule":"XXX",
	"id":5
	
}
"""

newsblog_meta = """
{
	"id":5
}
"""