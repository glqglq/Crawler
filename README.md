# 1.代码结构说明：
---
## 1.1 mycrawler：
子节点爬虫模块。实现了网页爬取、页面解析、正文抽取、自动摘要、关键词抽取、基于改进的布隆过滤器的URL去重、

## 1.2 web：
Flask交互模块和docker控制模块第一版。Flask交互模块实现了与用户交互和数据可视化，用户可以通过web前端输入信息和任务指令；爬取的数据也可以以表格的形式展示出来。

## 1.3 web2：
Flask交互模块和docker控制模块第二版。Flask交互模块实现了与用户交互和数据可视化，用户可以通过web前端输入信息和任务指令；爬取的数据也可以以表格的形式展示出来。


## 1.4 test：
测试文件夹，用于单元测试，部署时不必上传此文件夹。

# 2.部署环境：
---
## 2.1 硬件参数：
Intel(R) Xeon(R) CPU E5-2420 0 @ 1.90GHz   物理核数：6核  逻辑核数：24核   内存：24GB  硬盘：5TB

## 2.2 系统参数：
Centos 7
Python 2.7.5
Docker 17.03

# 2.部署步骤：
---
## 2.1 安装pip、setuptools并升级到最新版本
下载setuptools：

```
wget https://pypi.python.org/packages/6b/dd/a7de8caeeffab76bacf56972b3f090c12e0ae6932245abbce706690a6436/setuptools-28.3.0.tar.gz#md5=a46750b6bd90a1343466bd57b0e2721a
```


解压、安装setuptools：

```
tar zxvf setuptools-28.3.0.tar.gz
cd setuptools-28.3.0
python setup.py install3
```
下载pip：

```
wget https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-8.1.2.tar.gz#md5=87083c0b9867963b29f7aba3613e8f4
```
安装pip：

```
tar pip-8.1.2.tar.gz 
cd pip-8.1.2 
python setup.py install
pip install --upgrade pip
```


## 2.2 安装redis3.2.8

```
wget http://download.redis.io/releases/redis-3.2.8.tar.gz
tar -vxzf redis-3.2.8.tar.gz
cd redis-3.2.8.tar.gz
make
cd src
make install PREFIX=/usr/local/redis
cd ..
mkdir /usr/local/redis/etc
mv redis.conf /usr/local/redis/etc
vi /usr/local/redis/etc/redis.conf
将daemonize改为yes，将requirepass设置为1，将bind 127.0.0.1注释掉，将protected-mode改为no
vim /etc/rc.local
后面追加/usr/local/redis/bin/redis-server /usr/local/redis/etc/redis.conf
```

## 2.3 安装mongoDB
下载安装包：

```
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-3.4.4.tar
```
解压：

```
tar -xvzf mongodb-linux-x86_64-rhel62-3.4.4.tar
```
改名、转移：

```
mv mongodb-linux-x86_64-rhel62-3.4.4 mongodb 
mv mongodb /usr/local/mongodb
```
创建文件夹、文件：

```
cd /usr/local/mongodb
mkdir data
vi mongo.log
```

添加环境变量:

```
vi /etc/profile
```
添加export PATH=/usr/local/mongodb/bin:$PATH

```
source /etc/profile
mkdir /data/db
```
随机启动：

```
vim /etc/rc.local
```

添加/usr/local/mongodb/bin/mongod -dbpath=/usr/local/mongodb/data -logpath=/usr/local/mongodb/mongo.log --logappend --fo

## 2.4 构建docker子节点镜像：
拉取子节点镜像：

```
docker pull centos:7
```

在子节点镜像中执行以下命令：

```
yum install gcc libffi-devel openssl-devel libxml2 libxslt-devel libxml2-devel python-devel -y 
pip install scrapy scrapy-redis pymongo
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
tar -xvzf phantomjs-2.1.1-linux-x86_64.tar.bz2
vi /etc/profile
#添加以下一句话
export PHANTOMJS_HOME=/root/phantomjs-2.1.1-linux-x86_64
source /etc/profile
```

将mycrawler爬虫代码分发给各个子节点

## 2.5 在主机安装、开启Flask Web：
pip install Flask Flask-Script Flask-Bootstrap pymongo redis docker  

sudo nohup python mycrawl.py runserver --host 0.0.0.0 --threaded --port 10000

# 3.系统功能：
---
## 3.1首页：

系统控制面板，以图表的方式展示了：系统通知、任务状态、节点状态、爬取数据状态、服务器状态。

## 3.2添加节点：
新建并启动一个docker爬虫容器，开启对应的爬虫进程，等待分布式爬虫任务调度。

## 3.3节点状态：
对docker节点状态的封装，可以查看节点的id、名字、状态，也可以执行删除节点任务。

## 3.4添加任务：
可以添加电商类任务、新闻博客类任务。用户可以根据需求随意增添删除爬取项，针对不同的网站自己定义爬取规则。

## 3.5任务状态：
可以查看任务id、起始url、任务优先级、任务状态、任务类型、允许爬取的域名等。也可以进行状态修改：运行改为暂停、运行改为取消、暂停改为取消。

## 3.6新闻博客类爬取数据可视化：
可以实时显示爬取数据数量、爬取数据文件总大小，也可以点击详细数据，查看其抽取出的正文、摘要、关键词，甚至可视化词云。

## 3.7电子商务类爬取数据可视化：
可以实时显示爬取数据数量、爬取数据文件总大小，也可以点击详细数据看到添加任务时定义的规则所爬取出的对应项结构化数据。
