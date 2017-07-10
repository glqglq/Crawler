# -*- coding: utf-8 -*-

import sys,time,redis,pymongo,copy
from monitor.settings import REDIS_URL,BOT_NAME
from flask import Flask,render_template,flash,request,json,redirect
from flask_bootstrap import Bootstrap
from flask_script import Manager
from monitor.add_task import add_task
from monitor.node_manager import MyDocker
from monitor import continue_task,cancel_task,pause_task

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
redis_server = redis.StrictRedis.from_url(REDIS_URL)
my_docker = MyDocker()

#主页
@app.route('/')
def index():
    docker_status_json = my_docker.get_status()
    running_docker_count = 0
    for item in docker_status_json:
        if item['status'] == 1:
            running_docker_count += 1

    json = {
        'task_num':[redis_server.zcard('%s:running_task'%BOT_NAME),
                     redis_server.zcard('%s:done_canceled_task' % BOT_NAME),
                     redis_server.zcard('%s:pausing_task' % BOT_NAME)
        ],
        'node_num':[running_docker_count,len(docker_status_json) - running_docker_count]
    }

    return render_template('index.html', json = json)

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
        print dict_nodedelete
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

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500

if __name__ == '__main__':
	manager.run()
