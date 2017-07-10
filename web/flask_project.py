from flask import Flask, render_template

app = Flask(__name__)

from flask.ext.script import Manager
manager = Manager(app)

import json
from flask import request
from flask import redirect
from flask import jsonify

@app.route('/' , methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        a = request.get_data()
        dict1 = json.loads(a)
        return json.dumps(dict1["data"])
    else:
        return '<h1>post</h1>'

@app.route('/user/<name>')
def user(name):
    return'<h1>hello, %s</h1>' % name

@app.route('/sendjson/')
def sendjson():
    return redirect('testjson.html')

@app.route('/sendjson2/',methods=['POST'])
def sendjson2():
    data = json.loads(request.get_data())
    name = data["name"]
    age = data["age"]
    location = data["location"]
    data["time"] = "2016"
# Output: {u'age': 23, u'name': u'Peng Shuang', u'location': u'China'}
    print data
    return jsonify(data)

if __name__ =='__main__':
    manager.run()