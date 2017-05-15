# -*- coding: utf-8 -*-

import urlparse
import posixpath

from ..settings import ALLOWED_DOMAINS,TOP_LEVEL_DOMAINS
from scrapy.utils.url import parse_url

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

allowed_domains = ALLOWED_DOMAINS
top_level_domains = TOP_LEVEL_DOMAINS

IGNORED_EXTENSIONS = [
    # images
    'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
    'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

    # audio
    'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

    # video
    '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
    'm4a',

    # office suites
    'xls', 'xlsx', 'ppt', 'pptx', 'pps', 'doc', 'docx', 'odt', 'ods', 'odg',
    'odp',

    # other
    'css', 'pdf', 'exe', 'bin', 'rss', 'zip', 'rar',
]

def url_has_any_extension(url, extensions):
    return posixpath.splitext(parse_url(url).path)[1].lower()[1:] in extensions

def url_cleaning(url):
    # DONE 去掉href=""，去掉前置的/，去掉https://
    url = url[6:-1].lower()
    if url[:2] == r'//':
        url = url[2:]
    if r'https://' in url:
        url = url[8:]
    return url

def url_cleaning2(url):
    #DONE 前面加上http://
    if r'http://'not in url:
        url = 'http://' + url
    return url

def url_cleaning3(url):
    #DONE 处理allowed_domains
    for domain in allowed_domains:
        if url_has_any_extension(url,IGNORED_EXTENSIONS):
            return False
        if domain in url:
            return True
    return False

def url_cleaning4(url):
    # DONE 抽取出合法url，只允许前面是.或者/或者字母或者数字
    if url == '':
        return False
    flag = 0
    if url[0] == '.' or url[0] == '/' or url[0].isalpha() or url[0].isdigit():
        flag = 1
        if 'javascript' in url or '@' in url:
            flag = 0
    return flag == 1

def url_join(url_now,urls):
    for i in range(len(urls)):
        #是否是相对路径
        flag = 0
        for domain in top_level_domains:
            if domain in urls[i]:
                flag = 1
            if flag == 0:
                urls[i] = urlparse.urljoin(url_now,urls[i])
                break
    return urls

def all_url_cleaning(url_now,urls):
    #去掉href=""，去掉前置的//，去掉https://
    urls = map(url_cleaning, urls)
    #去掉前面的字符非英文字母或非.或非/或有非法字符的url
    urls = filter(url_cleaning4,urls)
    #将相对路径改为绝对路径
    urls = url_join(url_now, urls)
    #加上http://头
    urls = map(url_cleaning2, urls)
    #过滤掉非法domain
    urls = filter(url_cleaning3, urls)
    return urls

if __name__ == '__main__':
    urls = ['href="PL.CSS"',
    'href="PL.CSS"',
    'href="index.htm"',
    'href="company/company.htm"',
    'href="PRODUCTS/CLJ/CLJ.HTM"',
    'href="QUALITY/QUALITY.HTM"',
    'href="service/service.htm"',
    'href="link/link.htm"',
    'href="ly/ly.htm"',
    'href="PRODUCTS/CLJ/CLJ1910/CLJ1910.HTM"',
    'href="PRODUCTS/CLJ/CLJ1510A/CLJ1510A.HTM"',
    'href="PRODUCTS/CLJ/H-1000A/H-1000A.HTM"',
    'href="PRODUCTS/CLJ/H-2000B/H-2000B.HTM"',
    'href="PRODUCTS/CLJ/PL-1000D/PL-1000D.HTM"',
    'href="PRODUCTS/CLJ/PL-2000D/PL-2000D.HTM"',
    'href="PRODUCTS/CLJ/PL-3000D/PL-3000D.HTM"',
    'href="PRODUCTS/CLJ/PL-5000D/PL-5000D.HTM"',
    'href="PRODUCTS/CLJ/CLJ1910/CLJ1910.HTM"',
    'href="PRODUCTS/CLJ/CLJ1510A/CLJ1510A.HTM"',
    'href="PRODUCTS/CLJ/H-1000A/H-1000A.HTM"',
    'href="PRODUCTS/CLJ/H-2000B/H-2000B.HTM"',
    'href="PRODUCTS/CLJ/PL-1000D/PL-1000D.HTM"',
    'href="PRODUCTS/CLJ/PL-2000D/PL-2000D.HTM"',
    'href="PRODUCTS/CLJ/PL-3000D/PL-3000D.HTM"',
    'href="PRODUCTS/CLJ/PL-5000D/PL-5000D.HTM"',
    'href="LINK/LINK.HTM"',
    'href="http://www.pully.cn"',
    'href="COMPANY/COMPANY.HTM"',
    'href="COMPANY/COMPANY.HTM"',
    'href="index.HTM"',
    'href="COMPANY/COMPANY.HTM"',
    'href="LINK/LINK.HTM"',
    'href="http://www.miibeian.gov.cn"'
    ]
    print all_url_cleaning('http://www.pully.cn',urls)