FROM centos:7
MAINTAINER luckygong
RUN yum install wget bzip2 -y
RUN wget https://bootstrap.pypa.io/get-pip.py;python get-pip.py;rm -f get-pip.py
RUN yum install gcc libffi-devel openssl-devel libxml2 libxslt-devel libxml2-devel python-devel fontconfig -y
RUN pip install scrapy selenium jieba scrapy-redis pymongo
RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN tar -xvzf phantomjs-2.1.1-linux-x86_64.tar.bz2


# sudo nohup python mycrawl.py runserver --host 0.0.0.0 --threaded --port 10000 &