# -*- coding: utf-8 -*-

from scrapy.selector import Selector

# [
#     "XXX":{
#         "content_type":0,
#         "content_content":"XXX"
#     }
# ]

def getitemcontent(page_source,rules):
    """
    从网页中解析数据
    :param page_source: 
    :param rules: 
    :return: 
    """
    result = {}
    s = Selector(text=page_source)
    for rule in rules:
        if rules[rule]["content_type"] == 0:#xpath
            result[rule] = s.xpath(rules[rule]["content_content"] + r'/text()').extract()
        elif rules[rule]["content_type"] == 1:#class_name
            result[rule] = s.css('.' + rules[rule]["content_content"] + r'::text').extract()
        elif rules[rule]["content_type"] == 2:#css_selector
            result[rule] = s.css(rules[rule]["content_content"] + r'::text').extract()
        elif rules[rule]["content_type"] == 3:#id
            result[rule] = s.css('#' + rules[rule]["content_content"] + r'::text').extract()
        elif rules[rule]["content_type"] == 4:#link_text
            pass
        elif rules[rule]["content_type"] == 5:#name
            result[rule] = s.css(r"[name=%s]"%rules[rule]["content_content"] + r'::text').extract()
        elif rules[rule]["content_type"] == 6:#tag_name
            result[rule] = s.css(rules[rule]["content_content"] + r'::text').extract()
    return result