# 六十五： mysql语句执行原理：
### 第一步： 识别关键字 -->
    服务端会将sql查询语句放在一个线程当中运行，发送给mysql，到达sql后，mysql会首先判断sql语句的
    前六个字符是否是select,并且语句中不带有sql_no_cache关键字，符合条件，下一步就是查询缓存；
### 第二步： 查询缓存（mysql8.0之后取消缓存机制） -->
	缓存其实就是一张hash表，它将执行过的查询语句和结果以key-value的形式存储在内存中，key是由查询
    语句、数据库、客户端协议等生成的一个hash值，value是查询的结果；
	当然可以通过在查询语句中添加sql_no_cache关键字，或者将query_type_cache参数设置为demand绕过
    缓存；
	由于缓存具有一定的局限性，所有高版本mysql取消了缓存机制；
		局限1：sql语句一点点不同，都不会命中缓存（空格、注释等）；
		局限2：对一个 表的更新，会将所有缓存清空；
### 第三步： 解析器 -->
	缓存不命中情况下，进入解析器，解析器分两步对sql进行解析：
		解析步骤一：词法分析
		    从左往右一个字符一个字符地输入，然后根据构词规则识别单词，然后生成多个token；
		解析步骤二：语法解析
		    判断是否符合mysql的语法规则，如果不符合规则，抛出错误提示；如果语法正确，会生成一个语
            法树，送入到预处理器；
### 第四步： 预处理器 -->
     预处理器会对sql涉及的表名、列名、数据库等做匹配，看是否存在这些名字，不存在会抛出错误提示，然
     后再做权限验证，看是否具备操作权限，然后将这个语法树传递给优化器；
### 第四步： 优化器 -->
     优化器是针对语法树做优化，判断如何查询才能更快，生成一个执行计划，将执行计划交给执行器；
### 第五步： 执行器 -->
     执行器通过执行计划，一条一条的调用底层的存储引擎，逐步执行指令；
     mysql定义了一系列抽象的存储引擎API，支持插件式存储引擎架构。mysql实现了一个抽象接口层，叫做
     handler(sql/handler.h),其中定义了接口函数，比如：ha_open,ha_index_end,ha_create等等，存
     储引擎需要实现 这些接口才能被系统使用；
### 第六步： 返回结果
    最后，mysql会将查询的结果返回给客户端，如果是select类型的sql会将其缓存起来，其他类型的sql，会
    将该表涉及到的查询缓存清空（mysql8.0版本后取消缓存机制）；
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


# 五十六： mysql主从配置
**linux系统下配置my.cnf文件，windows下配置my.ini**

**mysql数据主从的复制是sql语句的复制，并不是真正意义上的数据复制，整个复制过程就是Slave从Master端获取bin-log日志然后在Slave中顺序的执行日志中所记录的sql操作**
### a. 主从的配置形式：
		一主一从
		主主复制
		一主多从 -- 可以增强系统读取的性能（读写分离）
		多主一从 -- 5.7版本开始支持
		联级复制

     配置主从的作用：
		实时灾备： 用于故障切换
		读写分离： 提供高效的查询服务
		备份： 避免宕机影响业务
     配置主从的必要条件：
	     主库开启binlog日志（设置log-bin参数）
	     主从server-id不同
	     从库服务器能连接上主库 
### b. 主从数据复制的原理：

	（1）主库生成一个binary log dump线程 -- 
	当从库节点连接主库节点时，主库会创建一个log dump线程，用于发送bin-log的内容，
    在读取bin-log的操作时，此线程会对主库上的bin-log加锁，当读取完成，发送给从节
    点之前锁会被释放；
	
	（2）从库生成一个I/O线程 -- 
	当从库节点上执行start slave命令后，从库会创建一个I/O线程用来连接主节点，请求
    主库中更新的bin-log.I/O线程接受到主库bin-log dump线程发送的更新之后，保存
    在本地的relay-log中；
	
	（3）从库SQL线程 -- 
	SQL 线程负责读取relay log 中的内容，检测到relay-log中新增了内容后，会解析成
    在主库中实际执行过的的操作并且执行，最终保证主从数据的一致性。

### c. mysql主从复制模式
**默认是异步模式，mysql增删改操作会全部记录在binary log中，当slave节点连接在master时，会主动从master处获取最新的bin log文件，并在从库解析、执行**

	（1） 异步模式 -- 主库不主动push bin log 到从节点（从库可能没
	                 有即时解析、执行最新的bin log）
	（2） 半同步模式 -- 主库收到一台从库返回的信息就会commit;
	（3） 全同步模式 -- 主从库都执行了commit并确认才会向客户端返回成功;
### d. 具体的主从配置实列（一主一从）
    (1)配置master数据库：

	编辑配置文件： vim /etc/my.cnf
	
	server-id = 200 # 设置主服务器的ID
	innodb_flush_log_at_trx_commit=2  # 操作系统崩溃或者低筒断电上一秒所有事务数据才可能丢失
	sync_binlog=1 # 开启binlog日志同步功能
	log-bin=mysql-bin-200 # binlog日志文件名
	binlog-do-db= 'database' # 这个表示只同步database数据库（没有这个配置表示同步所有）
	
	配置完成过后，重启mysql服务 ：  service mysql restart

	登录数据库：  mysql -uroot -p123456

	给slave数据库开通账号密码：
	grant replication slave on . to 'mark'@'192.168.1.201' identified by '123456' # 授权给从数据库服务器192.168.1.201，用户名mark,密码123456

	查看主库状态：
	show master status;     # slave数据库连接master数据库时有两个参数需要和File、Position一致

    (2)配置slave数据库

		编辑配置文件：  vim /etc/my.cnf
		
		server-id=201
		innodb_flush_log_at_trx_commit=2
		sync_binlog=1
		log-bin=mysql-bin-201
		
		配置完成后，重启mysql服务 ： service mysql restart
		
		登录mysql： mysql -uroot -p123456
		
		连接主数据库（master_log_file和master_log_pos分别是master中status中的File和Positon）： 
		 
		change master to master_host='192.168.1.200',master_user='mark' ,master_password='123456',master_log_file='mysql-bin-200.000002' ,master_log_pos=1167；
		
		开启从库： start slave;   (关闭从库： stop slave)
		
		查看从库状态： show slave status;
		
		如果slave_io_running和slave_sql_running 都是yes表示配置成功
# 五十五： Django_redis缓存
**除了redis以外,django有多种缓存方式，比如文件，内存，数据库等**
### a. 安装redis数据库
**为了安全，redis默认设置成保护模式，没有设置密码外网不能访问，可以将保护模式关闭或者设置密码，或者绑定ip**

		linux下安装：
		yum install redis
		查看服务：
		ps -ef | grep redis
		启动服务：
		service redis start
		客户端连接：
		redis-cli -p 6379 -h 127.0.0.1
		停止服务：
		service redis stop
### b. django中安装redis三方库：
        pip install django_redis 
### c. 在settins中配置CACHES缓存
**有多种方式缓存，比如全站缓存，页面缓存，session缓存，接口缓存等等，根据需要配置不同缓存类型，但是必须要有default默认缓存，没有这个会报错**

			CACHES = {
			 # 默认缓存
			 'default': {
				 'BACKEND': 'django_redis.cache.RedisCache',
				 'LOCATION': [
				     'redis://1.2.3.4:6379/0',
				 ],
				 'KEY_PREFIX': 'teamproject',
				 'OPTIONS': {
					 'CLIENT_CLASS': 'django_redis.client.DefaultClient',
					 'CONNECTION_POOL_KWARGS': {
					     'max_connections': 1000,
					 },
					 'PASSWORD': '123456',
				 }
			 },
			 # 页⾯缓存
			 'page': {
				 'BACKEND': 'django_redis.cache.RedisCache',
				 'LOCATION': [
				     'redis://1.2.3.4:6379/1',
				 ],
				 'KEY_PREFIX': 'teamproject:page',
				 'OPTIONS': {
					 'CLIENT_CLASS': 'django_redis.client.DefaultClient',
					 'CONNECTION_POOL_KWARGS': {
					 'max_connections': 500,
				 },
				 'PASSWORD': '123456',
				 }
			 },
			 # 会话缓存
			 'session': {
				 'BACKEND': 'django_redis.cache.RedisCache',
				 'LOCATION': [
					 'redis://1.2.3.4:6379/2',
				 ],
				 'KEY_PREFIX': 'teamproject:session',
				 'TIMEOUT': 1209600,
				 'OPTIONS': {
					 'CLIENT_CLASS': 'django_redis.client.DefaultClient',
					 'CONNECTION_POOL_KWARGS': {
					 'max_connections': 2000,
				 },
				 'PASSWORD': '123456',
				 }
			 },
			 # 接⼝数据缓存
			 'api': {
				 'BACKEND': 'django_redis.cache.RedisCache',
				 'LOCATION': [
				 	'redis://1.2.3.4:6379/3',
				 ],
				 'KEY_PREFIX': 'teamproject:api',
				 'OPTIONS': {
					 'CLIENT_CLASS': 'django_redis.client.DefaultClient',
					 'CONNECTION_POOL_KWARGS': {
					 'max_connections': 500,
				 },
				 'PASSWORD': '123456',
				 }
			 },
			}
### d. 在需要缓存的视图函数前加装饰器：@cache_page()
**如果是session缓存就不需要加装饰器**

		@cache_page(timeout=60,cache='api') # timeout是过期时间，cache指定缓存方式
		def test(request):
		    users = User.objects.all()
		    return render(request, 'test.html', {'users': users})
### e. 缓存的失效问题
**出现缓存失效的主要因素是高并发**

	一般情况下，我们设置缓存的过期时间都是比较规整的时间，比如1分钟、5分钟、10分钟等等，当并发很
	高时，可能会出现某一时刻同时生成很多的缓存，并且设了相同的过期时间，当过期时间到后，这些缓存
	同时失效，全部的请求转发到底层数据库中，得陈数据库可能就会崩溃（性能调到极优状态下的mysql支持的并发
	量在300-700，机械硬盘是300，固态硬盘是700）；或者是数据库中不存在的数据一直处在高并发压力下。

       缓存击穿 ： 当大量的缓存同时失效，导致同一时刻有大量的请求打到底层数据库；
	   缓存穿透 ：由于缓存区不存在查询数据，需要从数据库中查询，查不到数据则不写入缓存，这个
	            不存在的数据每次查询都会去数据库中查询，造成缓存穿透，这种查询出现高并发，就
	            会使数据库压力过大甚至瘫痪；
	      解决方法：
	     （1）布隆过滤器：将可能用于查询的所有数据以hash形式存储，位数组+k个独立hash函数。
                 将hash函数对应的值的位数组置一，查找时如果发现所位数组都是1，说明存在这个数据，否则不存在
	     （2）缓存空对象：无论数据库的返回是否为空，都缓存（可能会出现消耗更多的内存，或者被攻击也很严重，
                 可以设置较短的过期时间，或者在有数据填充这个空值时清除掉缓存中的空值）；
   
	   缓存雪崩：如果缓存集中在某一时间大面积失效（可能是缓存服务器崩溃，或者大面积缓存击穿，热点数据持续高并
                发等原因），新缓存未加载到内存，所有请求全打在底层数据库，造成底层数据库巨大压力
                严重的会造成数据库宕机，从而造成一系列的连锁反应，造成整个系统崩溃的缓存雪崩现象；
	            这个问题没有根本解决办法，但是可以分析用户行为，尽量让失效时间点均匀分布，大多数系统设
	            计者考虑用加锁或者队列的方式保证缓存的单线程，从而避免失效时大量的并发请求转
	            向底层的存储系统上。
             
      解决方法：
      （1）加锁排队 
          在缓存失效后，通过加锁或者队列来控制读数据库写入缓存的线程数量，比如对某一个key只允许一个
          线程查询数据和写入缓存，其他线程等待；业内常用mutex，简单的说就是在缓存失效时（判断拿出
          来的值是空），先使用缓存工具的某些成功操作返回值的操作（比如redis的setnx，只有不存在的时 
          候才设置，利用它来实现锁的效果）去设置一个mutex key；

          java代码如下：
			public String get(key) {  
			      String value = redis.get(key);  
			      if (value == null) { //代表缓存值过期  
			          //设置3min的超时，防止del操作失败的时候，下次缓存过期一直不能load db  
			          if (redis.setnx(key_mutex, 1, 3 * 60) == 1) {  //代表设置成功  
			               value = db.get(key);  
			                      redis.set(key, value, expire_secs);  
			                      redis.del(key_mutex);  
			              } else {  //这个时候代表同时候的其他线程已经load db并回设到缓存了，这时候重试获取缓存值即可  
			                      sleep(50);  
			                      get(key);  //重试  
			              }  
			          } else {  
			              return value;        
			          }  
			 }  
		（2）数据预热：
		   可以通过缓存reload机制，在即将发生大并发访问前手动触发加载缓存不同的key，设置不同的过期时间，
		   让缓存在失效的时间点尽量均匀，尽量不发生 在同一时间；

		（3）做二级缓存，或者双缓存策略（针对单点服务器故障可以配置redis主从、哨兵）：
		   A1为原始缓存，A2为拷贝缓存，A1失效时，可以访问A2，A1时间设置为短期，A2设置为长期；

		（4）缓存"永不过期"：
		   这里的永不过期在物理层面上来说，对缓存的key确实是没有设置过期时间，也就保证了不会因为缓存过期瞬间
		   出现的缓存穿透问题，但是从功能上来说，这种方式是将过期时间存在key对应的value当中，通过后台程序来
		   判断是否要过期了，当快要过期的时，通过后台的异步线程进行缓存的构建，也就是逻辑过期；从实际情况来
		   看，这种方式对性能非常友好，唯一不足的就是构建缓存时，其余线程可能访问的是老数据，但是对于一般的互
		   联网功能来说这个还是可以接受的。

