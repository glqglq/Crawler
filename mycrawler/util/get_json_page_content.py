# -*- coding: utf-8 -*-

from scrapy.selector import Selector

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# [
#     "XXX":{
#         "content_type":0,
#         "content_content":"XXX"
#     }
# ]

def getitemcontent(page_source,rules):
    """
    从网页中解析数据
    :param page_source: str类型，网页源代码
    :param rules: str类型，rules的json
    :return: 
    """
    # rules = eval(rules)
    # print page_source
    result = {}
    s = Selector(text=page_source)
    for rule in rules.get('itemcontents',None):
        try:
            if rules["type"] == 0:#xpath
                result[rule] = s.xpath(rules['itemcontents'][rule] + r'/text()').extract()[0]
            elif rules["type"] == 1:#class_name
                result[rule] = s.css('.' + rules['itemcontents'][rule] + r'::text').extract()[0]
            elif rules["type"] == 2:#css_selector
                result[rule] = s.css(rules['itemcontents'][rule] + r'::text').extract()[0]
            elif rules["type"] == 3:#id
                result[rule] = s.css('#' + rules['itemcontents'][rule] + r'::text').extract()[0]
            elif rules["type"] == 4:#link_text
                pass
            elif rules["type"] == 5:#name
                result[rule] = s.css(r"[name=%s]"%rules['itemcontents'][rule] + r'::text').extract()[0]
            elif rules["type"] == 6:#tag_name
                result[rule] = s.css(rules['itemcontents'][rule] + r'::text').extract()[0]
        except:
            pass
    return result