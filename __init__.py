# coding=utf-8
import urllib
import urllib2
import commands
import json

# from mycrawler.settings import SCRAPYD_URL,BOT_NAME,SPIDER_NAME
# from mycrawler.spiders.test_spider.test_spider import name



def start_all(nodes):
    """
    部署、运行所有节点的爬虫
    :param nodes:k-v形式，k对应scrapy.cfg中的名字，v是ip地址！ 
    :return: 
    """

    #部署
    for node in nodes.keys():
        deploy(node,node)

    #运行所有节点的所有spider
    for node in nodes.keys():
        schedule(url = nodes[node], project_name = node, spider_name = 'mycrawler', setting = None, jobid = None)

def deploy(target_name,project_name):
    """
    :param target_name:scrapy.cfg中的deploy:XXX 
    :return: 
    """
    commands.getstatusoutput('scrapyd-deploy %s -p %s'%(target_name,project_name)) #发布
    commands.getstatusoutput('scrapyd-deploy -L %s'%target_name) #验证是否发布成功


def schedule(url,project_name,spider_name,setting,jobid):
    """
        功能：调度爬虫爬取，返回jobid
        方法：POST
        json格式：{"status": "ok", "jobid": "6487ec79947edab326d6db28a2d86511e8247444"}
    """
    requrl = "http://%s:6800/schedule.json"%url
    test_data = {
        'project': project_name,
        'spider': spider_name,
        'setting' : setting,
        'jobid' : jobid,
    }
    test_data_urlencode = urllib.urlencode(test_data)
    req = urllib2.Request(url = requrl, data = test_data_urlencode)
    res_data = urllib2.urlopen(req)
    res = res_data.read()  # res 是str类型
    return json.loads(res)

def daemonstatus(url):
    """
        功能：获取爬虫状态
        方法：GET
        json格式：{ "status": "ok", "running": "0", "pending": "0", "finished": "0", "node_name": "node-name" }
    """
    requrl = "http://%s:6800/daemonstatus.json"%url
    req = urllib2.Request(requrl)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return json.loads(res)

def cancel(url,project_name,jobid):
    """
        功能：取消爬虫
        方法：POST
        json格式：{"status": "ok", "prevstate": "running"}
    """
    requrl = "http://%s:6800/cancel.json"%url
    test_data = {
        'project': project_name,
        'job' : jobid,
    }
    test_data_urlencode = urllib.urlencode(test_data)
    req = urllib2.Request(url = requrl, data = test_data_urlencode)
    res_data = urllib2.urlopen(req)
    res = res_data.read()  # res 是str类型
    return json.loads(res)

def listprojects(url):
    """
        功能：获得project列表
        方法：GET
        json格式：{"status": "ok", "projects": ["myproject", "otherproject"]}
    """
    requrl = "http://%s:6800/listprojects.json"%url
    req = urllib2.Request(requrl)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return json.loads(res)

def listspiders(url,project_name):
    """
            功能：获得spider列表
            方法：GET
            json格式：{"status": "ok", "spiders": ["spider1", "spider2", "spider3"]}
    """
    requrl = "http://%s:6800/listspiders.json"%url + "?project=%s"%project_name
    req = urllib2.Request(requrl)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return json.loads(res)

def listjobs(url,project_name):
    """
            功能：获得job列表
            方法：GET
            json格式：
                {"status": "ok",
                "pending": [{"id": "78391cc0fcaf11e1b0090800272a6d06", "spider": "spider1"}],
                "running": [{"id": "422e608f9f28cef127b3d5ef93fe9399", "spider": "spider2", "start_time": "2012-09-12 10:14:03.594664"}],
                "finished": [{"id": "2f16646cfcaf11e1b0090800272a6d06", "spider": "spider3", "start_time": "2012-09-12 10:14:03.594664", "end_time": "2012-09-12 10:24:03.594664"}]}
    """
    requrl = "http://%s:6800/listjobs.json?project="%url + project_name
    req = urllib2.Request(requrl)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return json.loads(res)