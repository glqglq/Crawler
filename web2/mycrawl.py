# -*- coding: utf-8 -*-

import sys,redis,copy,psutil
from monitor.settings import REDIS_URL,BOT_NAME
from flask import Flask,render_template,jsonify,request,json,redirect
from flask_bootstrap import Bootstrap
from flask_script import Manager
from monitor.add_task import add_task
from monitor.node_manager import MyDocker
from monitor import continue_task,cancel_task,pause_task
from monitor.get_task_data import get_newsblog_task_data,get_eb_task_data
from pymongo import MongoClient
from pymongo.errors import OperationFailure


reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

redis_server = redis.StrictRedis.from_url(REDIS_URL)
my_docker = MyDocker()
client = MongoClient()
db = client['admin']

#主页
@app.route('/index')
@app.route('/')
def index():
    docker_status_json = my_docker.get_status()
    running_docker_count = 0
    for item in docker_status_json:
        if item['status'] == 1:
            running_docker_count += 1

    task_ids = []
    task_ids += redis_server.zrange('%s:done_canceled_task' % BOT_NAME, 0, -1)
    task_ids += redis_server.zrange('%s:pausing_task' % BOT_NAME, 0, -1)
    task_ids += redis_server.zrange('%s:running_task' % BOT_NAME, 0, -1)

    eb_count,newsblog_count = 0,0
    for id in task_ids:
        this_task_information = eval(redis_server.hget('%s:task_information' % BOT_NAME,id))
        if this_task_information.get('type',None) == 1:
            for rule in this_task_information.get('rules',''):
                try:
                    stats = db.command('collstats', 'ebpagecontent_' + id + '_' + rule)
                    eb_count += stats.get('count',0)
                except OperationFailure:
                    pass
        elif this_task_information.get('type',None) == 0:
            try:
                stats = db.command('collstats', 'newsblogpagecontent_' + id)
                newsblog_count += stats.get('count', 0)
            except OperationFailure:
                pass

    # 弃用
    # json = {
    #     'task_num':[redis_server.zcard('%s:running_task'%BOT_NAME),
    #                  redis_server.zcard('%s:done_canceled_task' % BOT_NAME),
    #                  redis_server.zcard('%s:pausing_task' % BOT_NAME)
    #     ],
    #     'node_num':[running_docker_count,len(docker_status_json) - running_docker_count],
    #     'data_num':[eb_count,newsblog_count]
    # }

    num_task_r = redis_server.zcard('%s:running_task'%BOT_NAME)
    num_task_s = redis_server.zcard('%s:done_canceled_task' % BOT_NAME)
    num_task_p = redis_server.zcard('%s:pausing_task' % BOT_NAME)
    num_slave_r = running_docker_count
    num_slave_p = len(docker_status_json) - running_docker_count

    cpu_times = round(psutil.cpu_times().user,2)
    disk = round(float(psutil.disk_usage('/').used) / psutil.disk_usage('/').total * 100, 2)
    mem = psutil.virtual_memory()  # 内存信息
    neicun = round(float(mem.used) / mem.total * 100, 2)

    return render_template('index.html', num_task_r=num_task_r,num_task_p=num_task_p,num_task_s=num_task_s,eb_count = eb_count,
            newsblog_count = newsblog_count,num_slave_p=num_slave_p,num_slave_r=num_slave_r,cpu_times=cpu_times,disk=disk,neicun=neicun)

#添加节点
@app.route('/addslave',methods=['GET','POST'])
def addslave():
    result = 0  #0是添加失败，1是添加成功
    if my_docker.start_new_node():
        result = 1
    return render_template('add_slave.html',result = result)

#显示所有节点
@app.route('/listallslave',methods=['GET','POST'])
def listallslave():
    if request.method == 'POST':
        # TODO
        dict_nodedelete = request.form.to_dict()
        # print dict_nodedelete
        my_docker.delete_node(dict_nodedelete['id'])
        return render_template('list_all_slave.html')
    elif request.method == 'GET':
        jsonstr = my_docker.get_status()
        return render_template('list_all_slave.html',jsonstr = jsonstr)

#添加任务
@app.route('/addtask',methods=['GET','POST'])
def addtask():
    # 接收前端发来的数据,转化为Json格式,我个人理解就是Python里面的字典格式
    #[('alloweddomains', u'ict.ac.cn'), ('content_content.1.3', u''), ('content_content.1.2', u''), ('content_content.1.1', u''), ('key.1.4', u''), ('key.1.3', u''), ('key.1.2', u''), ('key.1.1', u''), ('content_content.1.4', u''), ('priority', u'20'), ('re_url.2', u''), ('re_url.1', u''), ('start_url', u'www.ict.ac.cn'), ('type', u'0'), ('type', u'0'), ('type', u'0')]
    if request.method == 'POST':
        # print request.form
        dict_form = request.form.to_dict()
        dict_task = {}

        dict_task['alloweddomains'] = dict_form['alloweddomains'].split(',')
        dict_task['priority'] = int(dict_form['priority'])
        dict_task['url'] = dict_form['start_url'] if ('http://' in dict_form['start_url']) or ('https://' in dict_form['start_url']) else 'http://' + dict_form['start_url']
        dict_task['type'] = int(dict_form['type'])
        if dict_task['type'] == 1:
            dict_task['rules'] = {}

            for item in dict_form:
                if 'rule_type' in item:
                    nowjson = {}
                    nownum = item[item.index('.') + 1:]

                    nowjson['itemcontents'] = {}
                    nowjson['type'] = int(dict_form['rule_type.'+nownum])
                    nowitemcontentcount = 1
                    while True:
                        if not dict_form.has_key('key.' + nownum + '.' + str(nowitemcontentcount)):
                            break
                        nowjson['itemcontents'][dict_form['key.' + nownum + '.' + str(nowitemcontentcount)]] = dict_form['content_content.' + nownum + '.' + str(nowitemcontentcount)]
                        nowitemcontentcount += 1
                    dict_task['rules'][dict_form['re_url.'+ nownum]] = copy.deepcopy(nowjson)
        # print dict_task
        add_task(redis_server,dict_task)
        return redirect('index')
    return render_template('add_task.html')

#显示所有任务
@app.route('/listalltask',methods=['GET','POST'])
def listalltask():
    if request.method == 'POST':
        dict_modechange = request.form.to_dict()
        if dict_modechange['prev'] == '0' and dict_modechange['next'] == '1': # pause=>run
            continue_task.continue_task(redis_server,int(dict_modechange['id'][5:]))
        elif dict_modechange['prev'] == '0' and dict_modechange['next'] == '2':# pause=>stop
            cancel_task.cancel_task(redis_server,int(dict_modechange['id'][5:]))
        elif dict_modechange['prev'] == '1' and dict_modechange['next'] == '0':# run=>pause
            pause_task.pause_task(redis_server,int(dict_modechange['id'][5:]))
        elif dict_modechange['prev'] == '1' and dict_modechange['next'] == '2':# run=>stop
            cancel_task.cancel_task(redis_server, int(dict_modechange['id'][5:]))
        elif dict_modechange['prev'] == '2' and dict_modechange['next'] == '0':# stop=>pause
            pass
        elif dict_modechange['prev'] == '2' and dict_modechange['next'] == '1':# stop=>run
            pass
        return render_template('list_all_task.html')
    elif request.method == 'GET':
        json_from_redis = redis_server.hgetall('mycrawler:task_information')
        jsonstr = []
        for item in json_from_redis:
            now_json = eval(json_from_redis[item])
            if redis_server.zscore('mycrawler:running_task',item):
                now_json['status'] = 1
            elif redis_server.zscore('mycrawler:pausing_task',item):
                now_json['status'] = -1
            elif redis_server.zscore('mycrawler:done_canceled_task',item):
                now_json['status'] = 0
            if now_json.has_key('type'):
                if now_json['type'] == 0:
                    now_json['type'] = '新闻博客类'
                else:
                    now_json['type'] = '电子商务类'
            temp = now_json
            temp['id'] = item
            jsonstr.append(temp)
        return render_template('list_all_task.html',jsonstr=jsonstr)

#显示所有新闻博客任务数据概览
@app.route('/listnewsblogdata',methods=['GET','POST'])
def getnewsblogdata():
    task_ids = []
    task_ids += redis_server.zrange('%s:done_canceled_task'%BOT_NAME, 0, -1)
    task_ids += redis_server.zrange('%s:pausing_task' % BOT_NAME, 0, -1)
    task_ids += redis_server.zrange('%s:running_task' % BOT_NAME, 0, -1)

    json = []
    for id in task_ids:
        this_task_information = eval(redis_server.hget('%s:task_information' % BOT_NAME,id))
        if this_task_information.get('type', '') == 0:
            json_temp = {}
            json_temp['type'] = "新闻博客类"
            json_temp['id'] = id
            json_temp['url'] = this_task_information.get('url','')
            try:
                stats = db.command('collstats', 'newsblogpagecontent_' + id)
                json_temp['count'] = stats.get('count','')
                json_temp['size'] = stats.get('size','')
            except OperationFailure:
                pass
            json += [json_temp]

    return render_template('list_all_newsblog_data.html', jsonstr = json)


#显示所有电子商务任务数据概览
@app.route('/listebdata',methods=['GET','POST'])
def getebdata():
    task_ids = []
    task_ids += redis_server.zrange('%s:done_canceled_task'%BOT_NAME, 0, -1)
    task_ids += redis_server.zrange('%s:pausing_task' % BOT_NAME, 0, -1)
    task_ids += redis_server.zrange('%s:running_task' % BOT_NAME, 0, -1)

    json = []
    for id in task_ids:
        this_task_information = eval(redis_server.hget('%s:task_information' % BOT_NAME,id))
        if this_task_information.get('type', '') == 1:
            for rule in this_task_information.get('rules',None):
                json_temp = {}
                json_temp['type'] = "电子商务类"
                json_temp['id'] = id
                json_temp['url'] = this_task_information.get('url', '')
                json_temp['re_type'] = rule
                try:
                    stats = db.command('collstats', 'ebpagecontent_' + id + '_' + rule)
                    json_temp['count'] = stats.get('count','')
                    json_temp['size'] = stats.get('size','')
                except OperationFailure:
                    pass
                json += [json_temp]

    return render_template('list_all_eb_data.html', jsonstr = json)


# 显示id为<id>的新闻博客类任务的格式化数据
@app.route('/listnewsblogdetaildata')
def getnewsblogdetaildata(name):
    next_page = int(request.args.get('next_page', '1'))
    task_id = int(request.args.get('id', '1'))

    return jsonify(get_newsblog_task_data(task_id,(next_page - 1)*10,next_page*10))

# 显示id为<id>的电子商务类任务的格式化数据
@app.route('/listebdetaildata/<id>')
def getebdetaildata(name):
    return render_template('list_all_eb_detail_data.html', jsonstr = json)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500

if __name__ == '__main__':
	manager.run()
