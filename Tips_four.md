# 六十八： python运行文件代码参数的区别：
**python运行文件时往往有三种方式：-u,-m,直接运行，可以通过python --help查看所有信息**
### 方式一（-m）：将一个模块当做脚本来运行；
	当前脚本所在的路径不会加入到sys.path列表中，但是sys.modules字典中的__main__
	路径是绝对路径，同时，还引入了runpy和pkgutil两个模块；
	
	runpy模块用途是定位并执行该模块，即实现命令行 -m 执行python模块的功能；
	pkgutil模块用途是获取包里面的所有模块列表，pkgutil.get_data()可读取包内
	任何文件内容；

    需要注意的是：在使用-m方式时，执行的脚本只用写文件名，不用写.py后缀；

        模块导入机制：
    模块的搜索路径保存在sys.path列表中，如果路径不存在其中，可以写代
    码加进去sys.path.append() ；
    所有加载到内存中的模块都存在sys.modules字典中；

    当import一个模块的时候，首先会在这个字典中查找是否已经加载了目标模块，如果已
    经加载，则将模块的名字加入到正在调用import的模块的local命名空间，也就是
    < module >.__dict__中，如果没有，则从 sys.path 查找，找到后载入内存，并加入
    到 sys.modules 字典，名称也将导入到当前模块的 Local 命名空间
### 方式二（直接运行脚本）：
	影响sys.path这个值，直接启动是把当前脚本路径加载到sys.path列表中，但是
	sys.modules字典中的__main__的路径不是绝对路径，是脚本名称；

### 方式三（-u）：将一个模块当做脚本来运行；
	默认情况下，标准错误（std.err）不缓存直接打印在屏幕，标准输出（std.out）需要
	缓存后再输出到屏幕；加上-u参数运行脚本，让脚本标准输出不缓存直接打印在屏幕上；

	sys.stdout.write("stdout1")
	sys.stderr.write("stderr1")
	sys.stdout.write("stdout2")
	sys.stderr.write("stderr2")
	直接运行的输出顺序：stderr1 stderr2 stdout1 stdout2
    加上-u参数运行的输出顺序：stdout1 stderr1 stdout2 stderr2
    
# 六十七： 进程管理工具 -- supervisor
**supervisor有网页版可视化管理界面，ip是布置supervisor工具的服务器ip,端口是默认端口3999，通过http://ip:3999可访问配置的supervisor**

	Supervisord是用Python实现的一款非常实用的进程管理工具。supervisord会帮你把管理的应用程序转成
    daemon程序，而且可以方便的通过命令开启、关闭、重启等操作，而且它管理的进程一旦崩溃会自动重启，这
    样就可以保证程序执行中断后的情况下有自我修复的功能。

	--> 安装supervisor: 可以下载安装包安装，也可以直接pip安装
	--> 两个类型的命令：supervisord和supercisorctl（安装完成后在/user/bin下）
	
	    配置supervisord: 
	    执行：echo_supervisord_conf > /etc/supervisord.conf 
	        （默认配置，如果权限报错，可以在其他文件生成再拷贝到/etc/supervisord.conf文件中）
             supervisord.conf文件中，可以配置日志文件最大值，和日志保存的文件数量等等，
             但是自带的日志配置只支持日志大小轮询，不支持以时间来轮询，可搭配logrotate管理日志；

	    添加需要守护的进程program：在supervisord.conf文件的最后加上以下代码：
          （也可以单独写一个配置进程的文件，包含进supercisord.conf文件中）
				[program:ice-0]   
				command=icegridnode --Ice.Config=config.grid
				directory=/package/second/new_image
				user=root
				autorestart=true
				redirect_stderr=true
				stdout_logfile=/package/second/new_image/log/ice_0.log
				loglevel=info
	     其中：ice-0是进程名
	          directory是进程项目的地址
	          command是进程项目启动命令
	          autorestart默认自动重启
	          stdout_logfile日志输出
        启动命令： /usr/local/bin/supervisord -c /etc/supervisord.conf 

        可以登录网址查看/管理 supervisor 运行状态：
             http://服务器ip:3999   (账号密码在supervisord.conf文件中有配置)
# 六十六： linux日志文件总管 -- logrotate（自动备份/轮询日志输出文件）
**logrotate可以自动对日志进行截断（或轮循）、压缩以及删除旧的日志文件，旧日志也可以通过电子邮件发送**
## 1. 创建 配置文件 -- touch /etc/logrotate.d/super_log
和大多数linux工具的配置文件一样，logrotate的配置文件是/etc/logrotate.conf，通常不需要对它进行修改。日志文件的轮循通常设置在独立的配置文件中，放在/etc/logrotate.d/目录下
## 2. 编辑 配置文件 -- vim /etc/logrotate.d/super_log
		/var/log/supervisor/super_log*.log {
		    daily
		    rotate 30  # num of backups
		    dateext
		    dateyesterday # 用昨天的日期做后缀
		    copytruncate
		    delaycompress    # today and yesterday will not compress
		    compress
		    missingok
		    notifempty
		}
    daily: 日志按天轮询。也可以设置为weekly/monthly/yearly；
	rotate: 备份文件个数，超过的会删除；
	dateext: 备份文件名包含日期信息；
	dateyesterday: 用昨天的日期做后缀,日志一般是凌晨备份前一天的数据，如果不用这个参数，日志文件显示的日期和实际不是一天；
	copytruncate: 首先将目标文件复制一份，然后再做截取（防止直接将原目标文件重命名引起的问题）；
	delaycompress ：与compress选项一起用，delaycompress选项指示logrotate不将最近的归档压缩，压缩将在下一次轮循周期进行 就是最新两个日志文档不压缩；
	compress： 压缩文件。如果不想压缩 可以和delaycompress 一起去掉；
	missingok： 忽略错误；
	notifempty： 如果没有日志 不进行轮询；
    还有其他参数，如（size/postrotate/endscript等）；
## 3. 测试是否配置成功 -- 
     logrotate /etc/logrotate.conf -- 调用logrotate.d下配置的所有日志配置文件
     logrotate /etc/logrotate.d/super_log -- 调用配置的单个日志配置文件
     logrotate -vf /etc/logrotate.d/super_log -- 即使轮循条件没有满足，也可以通过使用-f选项来强制logrotate轮循日志文件，-v参数提供了详细的输出
## 4. 简单用列： 与supervisor结合使用 --
**supervisor用于进程的管理，自带有日志的配置项，但是只能以文件大小来作为轮询条件，当需要用时间来作为轮询条件时，可以借助logrotate工具，比如每天/每周轮询等，需要注意的是，用logrotate配置轮询时，supervisor自带的轮询配置要关闭,比如以下配置：**

        supervisor的配置：
			# /etc/supervisor/conf.d/my_app.conf
			[program:my_app]
			directory=/opt/%(program_name)s
			command=/opt/%(program_name)s/run
			
			stderr_logfile=/var/log/supervisor/%(program_name)s_stderr.log
			stdout_logfile=/var/log/supervisor/%(program_name)s_stdout.log
			
			# 不设置日志文件大小（设置为0）
			stdout_logfile_maxbytes=0
			stderr_logfile_maxbytes=0
			
			# 不设置备份文件个数（设置为0）
			stdout_logfile_backups=0
			stderr_logfile_backups=0

        logrotate的配置：
			# /etc/logrotate.d/my_app
			/var/log/supervisor/my_app_*.log {
			    daily
			    rotate 30  # num of backups
			    copytruncate
			    delaycompress    # today and yesterday will not compress
			    compress
			    missingok
			    notifempty
			}

# 六十四:  nginx反向代理指定ip、端口简单设置
	server {
	  listen 4000;
	  server_name 192.168.2.99;
	
	  access_log /package/nginx_fra_logs/fra_access_0.log;
	  error_log /package/nginx_fra_logs/fra_error_0.log;
	
	  location / {
	      proxy_pass http://192.168.2.99:4000;
	  }
	}
# 六十三： python建立ice通信框架
### 1. 何为ice框架 -- 
    ice出自ZeroC,是一种面向对象的中间件平台，适合于异构平台环境中使用，客户端和服务器可以采用不同的编程语言，不同的操作系统
	    和机器架构，并且可以使用多种网络技术进行同信，可移植性高;Zeroc ICE( Internet Communications Engine)中间件号称标准统
	    一，开源，跨平台，跨语言，分布式，安全，服务透明，负载均衡，面向对象，性能优越，防火期传统，通讯屏蔽等多个优点，多种语言
	    之间采用共同的Slice进行沟通，支持C,JAVA,C#,VB,Python,Ruby,PHP等多语言映射。
### 2. ice框架搭建简介 -- 
	a. 安装ice -- pip install zeroc-ice
	b. 创建slice通信文件 -- 如：img.ice
	c. 在slice文件中建立module（详情请参照官方） -- 如下：
		module ImageRg
		{
		    sequence<byte> a;
		    sequence<a> b;
		    sequence<b> Images;
		    sequence<string> targetPlates;
		    sequence<string>  imageTimes;
		    sequence<string> illegalTypes;
		    sequence<string> imageDates;
		    sequence<string> pointsInfo;
		    sequence<string> targetLanes;
		    interface ImageDetection
		    {
		        string imagesRg(Images images,targetPlates plates, imageTimes time, illegalTypes type, imageDates date, pointsInfo point, targetLanes lane);
		    }
		
		}
    d. 生成ice编译库(slice2py命令，其他语言有对应命令) -- slice2py img.ice (会生成img_ice.py文件)
    e. 编写服务端代码：
		import Ice
        Ice.loadSlice('img.ice')
		class ImageDetection(ImageRg.ImageDetection):
			 def imagesRg(self, images, target_plates, image_times, illegal_types, image_dates, points_info, target_lanes, context=None):
			 return 'hello'
		with Ice.initialize(sys.argv, "config.server") as communicator:
		    adapter = communicator.createObjectAdapter("ImageA")
		    adapter.add(ImageDetection(), Ice.stringToIdentity('ImageRg'))
		    adapter.activate()
		    communicator.waitForShutdown()
    f. 编写客户端代码：
		import Ice
		import IceGrid
		Ice.loadSlice('img.ice')
		def run(communicator):
		    try:
		        base = communicator.stringToProxy("ImageRg")
		        aaa = ImageRg.ImageDetectionPrx.checkedCast(base)
		    except Ice.NotRegisteredException:
		        query = IceGrid.QueryPrx.checkedCast(
		            communicator.stringToProxy("ImageRgIceGrid/Query"))
		        aaa = ImageRg.ImageDetectionPrx.checkedCast(
		            query.findObjectByType("::ImageRg::ImageDetection"))
                result = aaa.imagesRg(img, target_plate, img_time, ill_type, img_date, point_info, target_lane)
                print(result)
		with Ice.initialize(sys.argv, "config.client") as communicator:
		    if len(sys.argv) > 1:
		        print(sys.argv[0] + ": too many arguments")
		        sys.exit(1)
		    run(communicator)
### 3. 易错点概括：
	a. ice文件moudle创建，相当于创建客户端和服务器通信的接口，定义接口函数时函数传递的参数的数据类型必须跟实际情况对应；
	b. 动态、静态生成编译库，静态生成指使用slice2py命令生成，动态生成指代码中生成Ice.loadSlice('img.ice')，实际开发两者可以一起使用
	c. ice均衡负载的配置，icegrid可以配置多个节点，节点配置易错，节点启动文件.xml文件配置，主节点config.grid、子节点node.conf配置 

# 六十二： pycharm通过ssh搭配docker进行远程服务器调试
**pycharm必须是professional版本才能进行远程ssh调试**

	第一步： docker容器配置ssh服务:
	    --> 创建容器: docker run 命令（必须有外部映射端口 -p 参数，允许外部连接到容器内部22端口）
		--> 进入容器： docker exec -it 容器名 bash
		--> 修改root密码：passwd
		--> 安装ssh服务（已安装则不需要）：apt-get install openssh-server/apt-get install openssh-client
		--> 修改ssh配置文件：vim /etc/ssh/sshd_config  :
		
			# PermitRootLogin prohibit-password # 默认打开禁止root用户使用密码登陆，需要将其注释
			RSAAuthentication yes #启用 RSA 认证
			PubkeyAuthentication yes #启用公钥私钥配对认证方式
			PermitRootLogin yes #允许root用户使用ssh登录
		
		--> 重启sshd服务：/etc/init.d/ssh restart

	第二步： pycharm配置远程调试：
	    -->点击pycharm左上方file - setting - project interpreter ；
		--> 新加一个远程的虚拟环境，点击右上角类似设置按钮的按钮下的 add；
		--> 配置远程地址：点击ssh interpreter , 填入 ip、端口、用户名，点击next；
		--> 输入远程服务器用户名的密码，点击next；
		--> 配置本地代码和远程代码的映射： 点击第二个输入框右边的文件夹图标、配置本地和远程代码路径；
		--> 配置完成后，确认，点击overwrite（本地代码更新会更新远程服务器的代码）；
        也可以在tools - deployment - configration中配置，配置完后，再设置远程虚拟环境

# 六十一： 如何动态获取mysql中一张表的字段名？
**从mysql自带的information_schema数据库的COLUMNS表获取**

    #  连接mysql数据库下的information_schema数据库（该数据库COLUMNS表存有所有数据库和表等相关信息）
    con = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='information_schema', port=3306)
    cursor = con.cursor()
    #  从information_schema表查询jd数据库下的goods表的字段名
    sql = 'select column_name from COLUMNS where table_name="goods" and table_schema="jd"'
    cursor.execute(sql)
    cols = cursor.fetchall()
    print(cols)  # (('id',), ('title',), ('img',), ('price',), ('sku',), ('detail',)) 存放查询到的每一条记录的字段信息
    columns_list = [i[0] for i in cols]  # 将数据库表的字段名组装成列表
    print(columns_list)
    con.close()
# 六十 ： yield 和 yield from简介
### a. yield可以写生成器和协程：
		生成器：
		def func(a):
		   for i in range(a):
		     yield i

		协程(yield作为参数传参)：
		def func():
		    while True:
		      x = yield
		      print(x)
		g = func()
		next(g) # 执行到yield,激活协程send(None）
		g.send(10) 
		g.send(20)
		g.send(30)
		g.close()
		
		输出：
		10
		20
		30
### b. yield from 指定返回的迭代对象（from后面跟可迭代对象）
		def func():
		   yield from [1,2,3]
		
		for i in func():
		   print(i)
		
		输出：
		1
		2
		3
	yield from的主要功能是打开双向通道，把最外层的调用方与最内层的子生成器连
	接起来，使两者可以直接发送和产出值，还可以直接传入异常，而不用在中间的协
	程添加异常处理的代码

# 五十九： linux的守护进程 -- 周期性执行任务或者等待处理某些发生的事件
**百度：守护进程是一类在后台运行并且不受任何终端控制的特殊进程，用于执行特殊的系统任务，很多守护进程在系统引导的时候启动，并且一直运行直到系统关闭，另外一些只在需要的时候才启动，完成任务后就自动结束**

	守护进程没有控制终端，因此当某些情况发生时，不管是一般的报告性信息，还是需要有管
	理员处理的紧急信息，都需要以某种方式输出，Syslog函数就是输出这些信息的标准方法，它
	把信息发送给syslogd守护进程，
	
	比如linux系统中很多以 .d 为后缀的文件，d就代表deamon，即守护进程，linux的大多数
	服务都是用守护进程实现的，比如xinetd提供网络服务，sshd提供ssh登录服务，vsftpd提
	供ftp服务器，httpd提供web服务等
	
	按照服务类型分为以下几种：
	
	1. 系统守护进程：syslogd、login、crond、at等；
	2. 网络守护进程：sendmail、httpd、xinetd、等；
	3. 独立启动的守护进程：httpd、named、xinetd等；
	4. 被动守护进程（由xinetd启动）：telnet、finger、ktalk等。


# 五十八： mysql数据备份
完全备份 ： mysqldump -u root -p --databases 数据库1 数据库2 > xxx.sql
           mysqldump -uroot -p -A > /data/mysqlDump/mydb.sql
增量备份 : 

# 五十七： python内置标准模块 -- 日志模块：logging
**主要用于输出运行日志，可以设置输出日志的等级、日志保存路径、日志文件回滚等**





