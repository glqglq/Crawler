# one.爬虫系统部署
## 0.关闭防火墙：
	
	暂时关闭：service iptables stop 
	永久关闭：chkconfig iptables off
	查询状态：service iptables status
## 1.将centos6.5的python2.6.6升级到python2.7.9
1.1.安装依赖：

		yum install bzip2 bzip2-devel -y
		yum install zlib zlib-devel -y
		yum install openssl openssl-devel -y

1.2. 解压、安装：

		wget https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz
		tar zxvf Python-2.7.9.tgz
		./configure
		make -j4
		make install

1.3配置：
		
        mv /usr/bin/python /usr/bin/python2.6_temp
		ln -s /usr/local/bin/python2.7 /usr/bin/python
		python -V  # Python 2.7.9
		vi /etc/profile
		# 添加如下内容：
		PY_HOME=/usr/local/bin/python2.7
		export PATH=$PY_HOME/bin:$PATH
		source /etc/profile  # 当前终端生效，reboot后才会完全生效
		echo $PATH
## 2.安装pip、setuptools并升级到最新版本
2.1下载setuptools：

       wget https://pypi.python.org/packages/6b/dd/a7de8caeeffab76bacf56972b3f090c12e0ae6932245abbce706690a6436/setuptools-28.3.0.tar.gz#md5=a46750b6bd90a1343466bd57b0e2721a

2.2解压、安装setuptools：

		tar zxvf setuptools-28.3.0.tar.gz 
		cd setuptools-28.3.0
		python setup.py install3
		
2.3下载pip：

		wget https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-8.1.2.tar.gz#md5=87083c0b9867963b29f7aba3613e8f4
	
2.4安装pip：

		tar pip-8.1.2.tar.gz 
		cd pip-8.1.2 
		python setup.py install
		pip install --upgrade pip
## 3.安装scrapy、scrapy-redis、bs4、MySQL-python、selenium、phantomjs：尝试一下内置
3.1安装scrapy、scrapy-redis、bs4、MySQL-python、selenium：
	pip install scrapy scrapy-redis MySQL-python
3.2安装phantomjs：
	wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
	tar -xvzf phantomjs-2.1.1-linux-x86_64.tar.bz2
	vi /etc/profile
	#添加以下一句话
	export PHANTOMJS_HOME=/root/phantomjs-2.1.1-linux-x86_64
	
## 4.安装redis3.2.8
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
## 5.安装mysql 5.7.17-1
5.1移除自带mysql：

	rpm –qa|grep -i mysql
	rpm –e MySQL-client-5.6.19-1.linux_glibc2.5.x86_64
	rpm -e MySQL-server-5.6.19-1.linux_glibc2.5.x86_64
	yum -y remove mysql-libs-5.1.73* 

5.2下载、解压mysql：

	wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.17-1.el6.x86_64.rpm-bundle.tar
	tar -xvf mysql-5.7.17-1.el6.x86_64.rpm-bundle.tar

5.3安装mysql：

	cd mysql-5.7.17-1.el6.x86_64.rpm-bundle
	rpm -ivh mysql-community-common-5.7.12-1.el6.x86_64.rpm   
	rpm -ivh mysql-community-libs-5.7.12-1.el6.x86_64.rpm   
	rpm -ivh mysql-community-client-5.7.12-1.el6.x86_64.rpm  
	rpm -ivh mysql-community-server-5.7.12-1.el6.x86_64.rpm  
	rpm -ivh mysql-community-devel-5.7.12-1.el6.x86_64.rpm  

5.4启动服务：

	service mysqld start 
	
5.5获得管理员密码：

	grep 'temporary password' /var/log/mysqld.log

5.6登陆、修改管理员密码：

	mysql -uroot -p
	ALTER USER 'root'@'localhost' IDENTIFIED BY '7758521123Pp!';
	
5.7授权远程登录并生效：

	grant all privileges on *.* to 'root'@'%' identified by '7758521123Pp!' withg rant option;
	flush privileges;
	
5.8更改默认编码为utf8：

	vim /etc/my.cnf，加入：
	[mysqld]
	character-set-server=utf8
	[mysql]
	default-character-set=utf8
	service mysqld restart重启mysql
	
5.9检查utf8编码设置：

	SET NAMES 'utf8';
	SET CHARACTER SET utf8;
	show variables like 'character\_set\_%';
	SHOW VARIABLES LIKE 'collation_%';
	status
## 6.建库、建表、加入初始爬取url：
6.1mysql建库、建表：

	CREATE DATABASE crawler DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
	CREATE TABLE pagecontent (
	Id int(11) NOT NULL AUTO_INCREMENT,
	url varchar(300) NOT NULL,
	content mediumtext NOT NULL,
	PRIMARY KEY (Id)
	) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
	alter database crawler character set utf8;
	alter table pagecontent convert to charset utf8 collate utf8_bin;
	alter table pagecontent convert to character set utf8 collate utf8_general_ci;
	
6.2redis插入初始url：

	lpush mycrawler:start_urls http://taobao.com
