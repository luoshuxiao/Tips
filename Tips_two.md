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

# 五十四： 浏览器的同源策略
### a. 概论
	浏览器的同源策略是由Netscape提出的一个安全策略，如今所有支持javascript的浏览器都会使用这个策略
	所谓同源， 是指域名，协议，端口相同，当一个页面加载或者执行一个脚本文件，需要打开另外一个地址，无
    论是接口还是网页都会检查要打开的地址是否是和当前地址同源，同源才会被执行，不同源不会被执行；
### b. CORS -- Cross Origin Rrsource Sharing 跨域资源共享
	方法一（不推荐使用，对自身服务器增加额外流量）：
		因为同源策略是限制js请求的，所以也有一种方式可以或者说可能可以解决这个问题，就是利用requests
        或者其他方式在服务器端获取数据，再调用这个数据进行操作或者直接渲染，实现数据的跨域请求利用；

    方法二（通常设置全部接口，资源共享）：
        配置cors跨域插件（安装插件： pip install django-cors-headers）
        在settings中配置：
        INSTALLED_APPS 中添加： 'corsheaders';
        MIDDLEWAER_CLASS 中添加： 'corsheaders.middleware.CorsMiddleware' #必须在django.middleware.common.CommonMiddleware'之前

        简单配置跨域资源具体权限：
        CORS_ORIGIN_WHITELIST = ('127.0.0.1:5000'，)  # 将允许访问本域的地址添加到白名单中
        CORS_ALLOW_CREDENTIALS = True
        CORS_ALLOW_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


            详细配置：
			#跨域增加忽略
			CORS_ALLOW_CREDENTIALS = True
			CORS_ORIGIN_ALLOW_ALL = True
			CORS_ORIGIN_WHITELIST = (
			    '*'
			)
			 
			CORS_ALLOW_METHODS = (
			    'DELETE',
			    'GET',
			    'OPTIONS',
			    'PATCH',
			    'POST',
			    'PUT',
			    'VIEW',
			)
			 
			CORS_ALLOW_HEADERS = (
			    'XMLHttpRequest',
			    'X_FILENAME',
			    'accept-encoding',
			    'authorization',
			    'content-type',
			    'dnt',
			    'origin',
			    'user-agent',
			    'x-csrftoken',
			    'x-requested-with',
			)

    方法三（通常设置部分个别接口资源共享）：
        在需要设置跨域资源共享的视图函数的响应头当中加入Access-Control-Allow-Origin参数，如下：
        response["Access-Control-Allow-Origin"]="http://127.0.0.1:8006"

        将共享的地址加入响应头当中，可以给指定的地址赋予访问权限，'*'代表所有地址都能访问，

        如下视图函数，表示这个接口可以被http://127.0.0.1:8080通过Ajax请求数据：

		def test(request):
		    users = User.objects.all()
		    response = render(request, 'test.html', {'users': users})
		    response["Access-Control-Allow-Origin"]="http://127.0.0.1:8080" # 在响应头添加共享域的地址
		    return response


# 五十三： select/poll/epoll
# 五十二： 如何配置HTTPS的SSL协议：
### a. 什么叫SSL协议：
**SSL全称Secure Sockets Layer，安全套接层**
为网络通信提供安全及数据完整性的一种安全协议，在传输层对网络连接进行加密；

### b. 服务器配置SSL协议：
**需要购买域名和SSL证书，域名备案成功，并购买SSL证书后，在阿里云将域名和SSL证书绑定配置好**

	nginx配置步骤：
	阿里官方：https://help.aliyun.com/knowledge_detail/95491.html?spm=5176.2020520154.cas.27.1cfbwTfiwTfiiX
	
	   --> 购买证书/域名(阿里云、腾讯云等等) 
       --> 在DNS中绑定SSL证书和域名（域名备案审批成功）
       --> 在证书界面验证证书 
       --> 下载公钥、密钥文件 
       --> 拷贝公钥、密钥到服务器上 
       --> 在/etc/nginx/文件夹下创建cert文件夹 
       --> 将解压后的公钥密钥文件拷贝到cert文件夹--> 检查并且修改cert文件的权限（不要给执行权限x，不安全）
       --> 备份nginx.conf文件（cp nginx.conf nginx.conf_back）
       --> 修改nginx.conf文件，增加443监听端口（或者在/etc/nginx/conf.d文件夹下创建一个.conf文件加入443的监听代码）
       --> 重启nginx服务 service nginx stop/service nginx start

       阿里官方给出的nginx配置SSL的代码如下：
       以下属性中ssl开头的属性与证书配置有直接关系，其它属性请结合自己的实际情况复制或调整；
				server {
				 listen 443;
				 server_name localhost;
				 ssl on;
				 root html;
				 index index.html index.htm;
				 ssl_certificate   cert/a.pem;
				 ssl_certificate_key  cert/a.key;
				 ssl_session_timeout 5m;
				 ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
				 ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
				 ssl_prefer_server_ciphers on;
				 location / {
				     root html;
				     index index.html index.htm;
				 }
				}
# 五十一： 可迭代对象、迭代器、生成器、生成式区别
## a. 可迭代对象：
**一个对象能够被迭代的使用，这个对象就是可迭代对象**

    容器是一种把多个元素组织在一起的数据结构，容器中的元素可以逐个的迭代获取，容器本身实际
    上并不支持取出元素的功能，而是由可迭代对象赋予了容器这种能力，比如列表中的元素获取，元
    祖、字典、集合等；

	python数据类型中，除了整型的基本数据类型都是可迭代对象，包括文件对象，python内部定义一个对象是不是可迭代对象的依据是，该对象是否存在__iter__()对象方法。
	
	所以判断一个对象是否是可迭代对象的方法有：
	方法一：
	from collections import Iterable
	isinstance(obj,Iterable) # 返回True表明是可迭代对象
	
	方法二：
	hasattr(obj,'__iter__')  # 返回True表明是可迭代对象
    因此：可以通过添加__iter__()方法让一个类的实列变为可迭代对象
## b. 迭代器：
**迭代器也是一种容器，并且是可迭代对象，因为迭代器是有\__iter\__()方法的，迭代器与可迭代对象的区别就在于，迭代器有\__next__()方法，而单纯的可迭代对象并没有这个方法**

	判断对象是是否是迭代器：
	方法一：
	from collections import iterator
	isinstance(boj,Iterator)  # 返回True表明是迭代器
	 
	方法二：
	hasattr(obj,'__next__')  # 返回True表明是迭代器
	
	迭代器可以通过内置函数next(obj)和obj.__next__()方法获取迭代器的下一个值，当迭代器的值
    取完了之后，再取会抛出StopIteration错误，但是可迭代对象并不能使用这两个方法
## c. 生成器（本质上来说就是一个迭代器）：
**一个利用yield返回结果的函数就是一个生成器，用iter(iterable)也可以生成一个生成器**

一般的函数在执行完毕之后会返回一个值然后退出，但是生成器函数会自动挂起，待下一次调用时，
 会在上次结束位置继续执行，实现了延迟计算,省内存

	斐波那契数列：
	def fib(max):
	    n,a,b =0,0,1
	    while n < max:
	        yield b
	        a,b =b,a+b
	        n = n+1
	    return 'done'
	 
	a = fib(10)  # 先调用生成器函数保存为迭代器对象，再获取元素，如果直接next(fib(10))，无论多少次next,只会拿到第一次元素
	for i in a:
	    print(i)

## d.生成式
**生成式是一种简单的生成器，返回一个迭代器对象，来源于迭代和列表解析的组合**

	列表解析式：
	a = [i for i in range(10)]
	
	生成式：
	b = (i for i in range(10))
	
	a和b主要有两点区别，第一就是a占用的内存比b大，第二就是a是通过遍历或者下标
	获取元素，b是通过遍历或者next获取元素
## e. for循环的遍历机制：
	可迭代对象是不可以直接从其中获取元素的，for i in obj遍历obj对象时，在for循环内部，被遍历
	的对象obj会首先调用__iter__()方法，将其变为一个迭代器，然后这个迭代器再调用其__next__()
	方法，返回取到的值给i，简单的说，for i in obj这句代码做的事就是：
           obj_iter = obj.__iter__()
	       i = obj_iter.__next__()  
    当然以上代码功能并不完整，因为for循环还自动捕捉了迭代器元素取完之后的StopIteration错误

    完整模拟for循环的内部机制的代码如下：

		l = [1,2,3,4,5]
		item = l.__iter__()  # 生成一个迭代器
		while True:
		    try:
		        i = item.__next__()
		        print(i)
		    except StopIteration:  # 捕获异常，如果有异常，说明应该停止迭代
		        break
## f. 反向迭代和迭代器切片操作：
### （1）反向迭代：
	python内置函数revered()可以实现可迭代对象的反向迭代：
	a = [1,2,3,4]
	b = reversed(a) # 此方法是生成一个a的反向对象，创建新的对象
	print(b)  # 输出：[4,3,2,1]
    等同于：
    a.reverse()  # 此方法是将a本身反向，并不创建新对象（只能引用于可变对象）
    如果实现了__reversed__()方法，就可以在自定义的类上实现反向迭代
### （2）迭代器切片：
    切片（islice方法）：
    import itertools
    a = (i for i in range(10))
    b = itertools.islice(a,3)  # 返回一个迭代器对象,类似 [:3]
    c = itertools.islice(a,3,None) # 返回一个迭代器对象，类似 [3:]
    c = itertools.islice(a,3,6) # 类似 [3:6]
    注意： islice会消耗迭代器，经过切片的迭代器会将切片部分以及切片之前的元素去掉，
          设置了None的islice会将原迭代器全部消耗掉：
			b = (i for i in range(10))  # 如果b是列表，用islice不会消耗该列表
			c = itertools.islice(b,3,None)
			print([i for i in c])  # 输出 [3, 4, 5, 6, 7, 8, 9]
			print(next(b))  # 抛出StopIteration错误

    去特定元素（dropwhile方法）：
    import itertools
    with open('test.py','r') as f: 
      for line in itertools.dropwhile(lambda x:x.startswith('#'), f):  # 遍历不是以#开头的所有行
           print(line)

    其中：itertools.dropwhile(lambda x:x.startswith('#'), f)表示删除f中以#开头的行，返回其他行的迭代器

# 五十： 如何读取大文件（10G/100G级别）进行处理？
		方法一（写迭代器，一行一行读取）：
		def open_line(filename):
		   with open(filename,'r') as f:
		      for i in f:  # 一行一行遍历
		         yield i  # 返回一行数据
		注意： 这种方式适合行数多的大文件（如果这个大文件只有一行，这种方式也不能处理）
		
		方法二（写迭代器，一块一块读取）：
		def open_piece(filename):
		   piece_size = 1024*1024*1024  # 表示一个G
		   while True:
		      with open(filename,'rb') as f:
		           block = f.read(piece_size)  # 每次读取piece_size大小的文件（以二进制读取会提高速度）
		           if block:
		               yield block.decode('utf-8') # 返回字符串
		           else:
		             return
        方法三（用pandas，一块一块读取,获取整个文件的迭代对象）：
        import pandas as pd
        data = pd.read_table(filename,sep='|',chunksize=400) # 返回迭代对象，对象每个元素是filename文件的400行数据
        for i in data:   # 遍历data,  i表示400行数据 ，也可以使用next(data)或者data.__next__()方法获取
            for j in i:  # 遍历i, 拿到每一行数据
               print(j)  # 处理每一行数据
            
        注意：使用与csv等数据类型文件
# 四十九： python中的with关键字
**文件、数据库连接、socket、线程、进程等系统资源，应用程序打开这些资源并执行完业务逻辑后，必须释放这些资源，可以通过资源对象的close()或其他方法关闭资源，但是比较繁琐，开发中也容易忘记关闭资源，with关键字对资源管理提供了方便**
### a. 文件的打开，关闭：
	def open_file_close():
	    f = open('test.txt','r')   # 当然，也可以写try/except/finally在finally中关闭资源
	    data = f.read()
	    f.close()

但是并没有用with关键字更加优雅简洁、更加方便：

	def with_file():
	    with open('test.txt','r') as f:
	        data = f.read()
	with语句会自动打开文件，并将对象以f别名返回，在处理完后，自动关闭资源

### b. with的实现原理（上下文管理器）：
**任何实现了\_enter\_()和\_exit\_()方法的对象都可以称之为上下文管理器，任何对象，只要正确实现了上下文管理，就可以使用with来进行管理**

	当一个对象的父类中定义了__enter__()和__exit__()方法，就可以用with关键字来进行该对象的资源管理
	with关键字首先会寻找资源对象父类中是否有__enter__()和__exit__()方法,如果有则会调用__enter__()
	方法，__enter__()方法一般都是打开资源返回资源对象，当with下的业务逻辑处理完，就会自动调用__exit__()方法
	方法，一般处理一些释放资源的清除工作，当我们要自定义一个上下文管理器，用with进行管理时，编写
	__enter__()必须要有返回值，编写__exit__()方法传入的参数必须是4个（包括self），如果__exit__()
    方法返回True，表示with-body中的代码出现异常时，忽略异常继续执行，返回False向上层抛异常
### c. with实现线程锁资源的管理
	import threading
	import time
	num = 0
	mutex=threading.Lock()
	class Mythread(threading.Thread):  # 生成线程类
	    def run(self):
            global num
	        with mutex:   #  用with关键字实现锁的自动添加和自动释放，代替锁的acquire()和release()方法
	          for i in range(100):
	             num+=1
	        print(num)
	my_list = []
	for i in range(5):
	   t = Mythread()
	   t.start()
	   mythread.append(t)
	for t in mythread:
	   t.join()
	print('finished')
### d. 自定义资源管理器类（可以用with进行管理）
	class A():
	    def __enter__(self):
	        self.a=1
	        return self
	    def f(self):
	        print('f')
	    def __exit__(self,a,b,c):
	        print('exit')
	
	with A() as a:
	    1/0     # 当with下的代码有异常时，如果__exit__()返回True，程序忽略错误，执行__exit__()中的代码
                # 如果__exit__()返回False,会抛出错误执行__exit__()方法，终止程序（但with并不能捕捉错误）
	    a.f()
	    print(a.a)
### e. contextlib模块（让对象实现上下文管理器来支持with）
contextlib模块提供了三个对象:contextmanager装饰器，nested函数和上下文管理器closing，可以对已有的生成器函数或者对象进行包装，加入上下文管理协议来支持with语句

##### one -- 装饰器contextmanager --
 
@contextmanager让我们通过编写generator生成器函数来简化上下文管理，可以实现执行一段代码之前做一些业务逻辑，在
执行这段代码之后，再执行一些业务逻辑的功能

	用于对生成器函数进行装饰返回一个上下文管理器，它的__enter__()和__exit()__方法由contextmanager负
	责提供，被装饰的生成器只能返回一个值（yield关键字后面只有一个返回值），否则会导致异常，产生的值会赋
	值给as子句中的target变量（如果使用了as子句）
	
				from contextlib import contextmanager
				@contextmanager
				def tag(name):
				    print("<%s>" % name)
				    yield
				    print("</%s>" % name)
				
				with tag("h1") as f:
                    print(f)
				    print("hello")
				    print("world")
	
			以上代码的执行顺序是：
			1. with语句首先执行yield之前的语句，因此打印出<h1>；
			2. yield调用会执行with语句内部的所有语句，因此打印f的值，由于yield没有返回值，
			   则会打印None，再打印hello和world；
			3. 最后执行yield之后的语句，打印出</h1>。
##### two -- nested()函数 -- 
将多个上下文管理器组织到一起，避免with的嵌套

注意： 如果发生异常，某个上下文管理器的 \__exit\__() 方法对异常处理返回 False，上层管理器监测不到异常
      则更外层的上下文管理器不会监测到异常

        比如以下代码：
		with nested(A(), B(), C()) as (X, Y, Z):
		     print('ABC')

		等价于：
		with A() as X:
		    with B() as Y:
		        with C() as Z:
		             print('ABC')
##### three -- closing上下文管理器
closing适用于有close()方法的对象（否则会报AttributeError 错误），比如网络连接、数据库连接等，通过接口close()来执行所需要的资源“清理”工作

	class ClosingDemo(object):
	    def __init__(self):
	        self.acquire()
	    def acquire(self):
	        print('init 调用')
	    def free(self):
	        print('close调用')
	    def close(self):
	        self.free()
	 
	with closing(ClosingDemo()):
	    print('with_body执行')
		
	执行结果：
	init 调用
	with_body执行
	close调用

# 四十八： python连接mysql/mongodb/redis
### 1. 连接mysql数据库(pymysql和sqlalchemy) -- 

	通过pymysql连接mysql数据库:

	    import pymysql
	    host = '127.0.0.1'
	    port = 3306
	    user = 'root'
	    password = '123456'
	    database = 'mogujie'  # mysql中数据库的名字
	    db = pymysql.connect(host, user, password, database, charset='utf8', port=port)  # 建立连接
	    cursor = db.cursor()  # 获取游标对象
	    sql = "select * from table_goods where id=1;"  # 需要执行的sql
	    sql1 = "insert into table_goods (name,price) values (%s,%s)"  # 需要执行的sql
	    cursor.execute(sql,("shoes",100))  # 执行sql
	    db.commit()  # 提交事务
	    db.close()  # 关闭连接

    通过sqlalchemy建立model连接数据库：

	    from sqlalchemy.orm import sessionmaker
	    from sqlalchemy import create_engine
		from sqlalchemy.ext.declarative import declarative_base

		Base = declarative_base()
		class Goods(Base):
		    __tablename__ = 'goods'   #映射的数据库表名
		    id = Column(Integer, primary_key=True, autoincrement=True)    # 主键自增
		    title = Column(String(128))
		    img = Column(String(1024))
		    price = Column(String(32))


        engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/mogujie?charset=utf8") # 建立连接
        Session = sessionmaker(bind=engine)  #Session()可以创建一个绑定到数据库的对象。但是到此为止，它还没有打开任何的连接
        session = Session  #当它第一次被调用的时候，会尝试从数据库引擎连接池中检索一个链接，该连接会一直被持有直到所有的任务都被提交或者Session对象被关闭
        goods = Goods()
        goods.title = '衣服'
		goods.img = '111.png'
		goods.price = '100'
        session.add(goods)
        session.commit()
### 2.连接mongodb数据库（pymongo/mongoengine）
		from pymongo import MongoClient
		client = MongoClient()  # client = MongoClient('mongodb://127.0.0.1:20719') 建立连接
		db = client.mogujie  # db = client['mogujie'] 获取数据库对象
		coll = db.goods  # coll = db['goods']  获取集合对象
		coll.insert_one({"name":'裤子'})  # 插入数据
		coll.insert_many([{'name':'裤子'},{'name':'衣服'}]) # 插入数据
		coll.find() # 查询所有数据
### 3.连接redis数据库
		import redis
		pool = redis.ConnectionPool(host='127.0.0.1',password='123456') # 实现一个连接池
		r = redis.Redis(connection_pool=pool)
		r.set('foo','bar')
		foo = r.get('foo')
		
		set(name, value, ex=None, px=None, nx=False, xx=False)
		　　在Redis中设置值，默认，不存在则创建，存在则修改
		　　参数：
		     　　ex，过期时间（秒）
		     　　px，过期时间（毫秒）
		     　　nx，如果设置为True，则只有name不存在时，当前set操作才执行
		     　　xx，如果设置为True，则只有name存在时，岗前set操作才执行
# 四十七：二叉树的前、中、后、序排列
**根据根节点的排序位置分为前中后**

	前序排列：根、左、右（根节点在前面，由上向下排序）
	中序排列：左、根、右（根节点在中间，左边自上而下排序，右边自下而上排序）
	后序排列：左、右、根（根节点在最后，左右都自下而上排序）

# 四十六：python时间格式化
### 1. 格式化时间：
	输出当前时间（字符串）：
	datetime.datetime.now()   # 输出：2019-03-30 12:47:33.595671
	datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 输出：2019-03-30 12:47:33
    
### 2. 时间戳转字符串：
	输出当前时间（时间戳）：
	seconds=time.time() # 输出：1553921431.3428378
    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(seconds)） # 输出：2019-03-30 12:58:55
    time.mktime(time.strptime("2018-08-07", "%Y-%m-%d")) # 输出：1533571200.0
# 四十五： \_\_new\_\_和\_\_init\__的区别和关联：
**特别注意：python类实例化时默认（自身未重构\__new\__）都是调用父类的\__new\__方法，不会也不能调用自己的\__new\__方法，避免陷入死循环**
## 1. 区别：
### a. 调用顺序先后 -->  实例化时，先调用\__new\__方法，后调用\__init\__方法
### b. 类别不同 --> \__new\__是类的静态方法（实例化方法），\__init\__是对象方法（构造方法）
### c. 功能不同 --> \__new\__是将类实例化的方法，\__init\__是接受\__new\__参数和返回的实例化对象，构造并且初始化对象，所以也叫对象的初始化方法
### d. 调用方式不同 --> 类实例化（自身未重构\__new\__）调用父类的\__new\__方法，初始化对象调用的是自己的\__init\__方法

## 2. 联系（四种特殊情况）：
### a. 默认情况：
	python源码默认的是实例化方法__new__在对象实例化时首先被调用，如果没有重构，默认是调用父类的实例化
	方法，父类也没有重构，再调用父类的父类，直到基类object的__new__方法，返回父类构造的实例化
	对象和实例化时接受的参数给__init__方法对对象进行初始化构造；
### b. 重构\__new\__方法，正常返回该类实例化对象和接受的参数：
	如果程序员自定义重构了要实例化类的__new__方法，实例化时就不调用父类的__new__方法，并且
	重构的__new__方法正常返回，即返回父类的实例化对象和接受的参数给__init__，那么正常初始化
	构造该类的实例化对象；
### c. 重构\__new\__方法，不返回实例化对象
    如果重构的__new__方法不返回当前类的实列对象，那么当前类的__init__方法不会被调用；
### d. 重构\__new\__方法，返回其他类的实例化对象
    如果__new__方法返回其他类的实列对象，那么只会调用被返回对象的所属类的__init__方法。

# 四十四： Session/Cookie/Token：
**参考 -- https://www.cnblogs.com/moyand/p/9047978.html**
### a. 为什么有这三个东西：
	很久以前，或者说一直以来，WEB的访问都是无状态访问，意思就是用户访问页面，但是
	WEB并不能保存用户的相关状态信息，每次请求都是全新的，后来随着交互式WEB应用的兴起，
	像在线购物网站等，需要记录用户的状态和相关信息，引入了会话标识（session id）,但是
	访问量过大时，服务器 需要保存大量的会话标识，是一个巨大的开销，为了更好的解决这些问
    题，经过几次技术的更新，让每个客户端去保存会话标识，引入Cookie作为客户端保存标识的
    对象，又引入令牌Token和标签做用户状态验证功能；
### b. 名词解析：
##### （1）Session  -- 
	字面上讲，就是会话，服务器要知道当前发送请求给自己的是谁，就要给每个哭护短分配不同的身份标
	识，让客户端每次请求带上身份标识（通常就是uer_id），服务器就知道这个请求来自于谁，客户端保
	存身份标识的方式普遍都是Cookie，服务器使用Session把用户的信息临时保存在服务器上（可以是服
	务器数据库，或者缓存区等），用户离开网站Session会被销毁，或者保存一定时间（可以设置，django
	默认过期时间是14天），这种存储方式相对Cookie跟安全，但是也有缺点，比如当服务器做了均衡负载
	时，用户下一个请求到了另外一台服务器Session就会丢失，也就是说另外一个服务器并不存在这个客户
	的Session，就会让客户再次登录，这大大降低客户的体验度；

			Session丢失的解决方案：
			第一种 -- 粘性Session：
				  将同一用户的请求固定在同一台服务器，不在各服务器之间做轮询，优点是很简 
				  单，不用改session只需要在负载均衡服务器中配置下轮询的规则就可以，缺点
				  也很明显，如果固定的那台服务器挂了，请求转到另外一台服务器上，那么一样
				  会再次让客户登录；
			
					nginx中配置ip_hash轮询方式来达到粘性session功能:
					upstream mycluster{
					   ip_hash;  # 添加一个ip_hash
					   server 192.168.22.229:8080 weight=1;
					   server 192.168.22.230:8080 weight=1;
				}
			
			第二种 -- 服务器之间复制session: 
			      任何服务器session更改都将其session所有内容序列化复制广播给其他服务器，保证
			      session同步，优点是有容错性，不受单点服务器影响，缺点是对网络负荷造成压力，
			      如果session量大，拖慢服务器性能，甚至可能拖垮服务器；
			
			第三种 -- session数据共享机制 ： 
			     使用分布式缓存方案（memcached/redis等，缓存必须是集群）
			
			第四种 -- session持久化到数据库 ： 
			     拿一个数据库专门保存session,优点是session不会受服务器影响,缺点是访问量过大时，
			     对数据库造成很大压力，会增加额外开销维护数据库；
			
			第五种 -- Terracotta实现session复制 ：
			     Terracotta（java开源集群平台）的基本原理是对于集群间共享的数据，当在一个节点
			     发生变化的时候，Terracotta只把变化的部分发送给Terracotta服务器，然后由服务
			     器把它转发给真正需要这个数据的节点
##### （2）Cookie -- 
		Cookie是一个很具体的东西，是浏览器实现的一种数据存储功能，能永久或者短暂存储
		一种数据的小文本文件，可以包含有关用户的信息，包括Token和其他信息，cookie由服
		务器生成，浏览器以KV形式保存到文件中，下一次请求同一网站时会把该cookie发送给服
		务器，由于cookie是存在客户端上的，所以浏览器加入了一些限制确保cookie不会被恶意
		使用，同时不会占据太多磁盘空间，所以每个域的cookie数量是有限的；

##### （3）Token --

		web领域中基于Token的身份验证随处可见，在大多数使用web API的互联网中，Token是多
		用户下处理认真的最佳方式，这种验证方式是将验证信息放在客户端，将验证规则放在服务
		端，以时间（计算验证Token）换空间(存储验证信息)的方式，既保证了服务器的安全性，
		又减小了服务器因session而浪费的空间；
		
			特点如下：
				1.无状态、可扩展
				2.支持移动设备
				3.跨程序调用
				4.安全

### c. Session/Cookie/Token用户状态验证的原理：
	用户第一次用户名、密码登录成功后，服务器定义并存储该用户身份标识存在session中（一般是
    程序员编码实现，通常用user_id做标识），产生一个令牌Token(包含用户身份标识user_id),
    并且通过算法和加密生成一个标签，将标签和令牌token一起发送给客户端，标签作用是避免有人
    伪造Token,让标签和Token成对匹配，因为算法和加密只有服务器知道（当然别人可以直接获取到
    Token），客户端收到Token保存在本地的Cookie中，每次请求（未退出登录）将Token放在请求
    头header中，服务器收到Token后，运用相应的算法和加密解析出Token中的签名，与Token自带
    的签名作比较，如果相同说明验证成功，该用户已经登录过了，如果不同，数据部分肯定被人篡改
    过，服务器做出相应的回应。

# 四十三： 单例模式
**单例模式是一种常用的软件设计模式。核心结构中只包含一个被称为单例类的特殊类。单例模式可以保证系统中单列类只有一个实例而且该实例易于外界访问，从而控制实例个数节约系统资源。如果希望在系统中某个类的对象只能存在一个，单例模式是最好的解决方案（创建唯一对象）**

    方法一（重构构造函数__new__）：
		创建单列类(非线程安全)：
		class SingletonNoSafe(object):
		     def __new__(cls,*args,**kwargs):
		           if not hasattr(cls,'_instance'):  # 判断是否已经创建单列对象
		              cls._instance = object.__new__(cls)
		           return cls._instance
		s = SingletonNoSafe()
		b = SingletonNoSafe()
		print(id(s))  # 39872216
		print(id(b))  # 39872216 两个对象的地址相同，说明是同一个对象
	
	    创建单列类（线程安全）：
	    import threading
	    class SingletonSafe(object):
	         _instance_lock = threading.Lock()
	         def __init__(self):
	              pass
	         def __new__(cls,*args,**kwargs):
	              if not hasattr(cls,'_instance'):  # 判断如果单列类没有创建对象，才执行
	                 with SingletonSafe._instance_lock:  # 打开线程锁
	                      if not hasattr(cls,'_instance'):  # 判断如果单列类没有创建对象，才执行
	                          cls._instance = object.__new__(cls) # 通过父类生成实列
	              return cls._instance 
	    s = SingletonSafe()
		b = SingletonSafe()
		print(id(s))  # 39370088
		print(id(b))  # 39370088 两个对象的地址相同，说明是同一个对象

    方法二(python模块化管理创建单列对象)：
		# mysingleton.py （在一个文件写单列类，创建单列对象）
		class My_Singleton(object):
		    def foo(self):
		        pass
		my_singleton = My_Singleton()
		
		# to use （在另外一个文件使用单列对象，其他地方不能再用单列类创建对象）
		from mysingleton import my_singleton
		my_singleton.foo()   # 只存在一个对象，如果再生成一个对象，就破坏了单列模式

    方法三（装饰器生成单列类）：
	    from functools import wraps
	    def singleton(cls):
	       instances = {}
	       @wraps(cls)
	       def _singleton(*args,**kwargs):
	           if cls not in instances:
	               instances[cls] = cls(*args,**kwargs)
	           return instances[cls]
	       return _singleton
	
	    @ singleton
	    class SelfClass(object):
	       pass
	    s = SingletonSafe()
		b = SingletonSafe()
		print(id(s))  # 39810552
		print(id(b))  # 39810552 两个对象的地址相同，说明是同一个对象

    方法四（属性共享）：
		class Singleton(object):
		   states = {}
		   def __new__(cls,*args,**kwargs):
		       obj = object.__new__(cls,*args,**kwargs)
		       obj.__dict__ = cls.states
		       return obj
		a = Singleton()
		b = Singleton()
		printe(id(a))  # 39654904
		printe(id(b))  # 39655016 两个对象地址不一样
		print(b.__dict__) # {}
		print(a.__dict__) # {} 但是两个对象的所有属性和对象方法一样，也就是将所有属性和方法指向
		                  #     相同属性和方法，实现单列模式

# 四十二： python常用内置函数
	1. abs() -- 求绝对值 
	2. isinstance(obj1,obj2) --判断两个对象类型是否一致(考虑继承关系，承认子类和父类类型一致)
	3. type(obj) -- 判断两个对象类型是否一致（不承认子类和父类类型一致）
	4. divmod -- 除法和求余数的结合 (被除数，除数)
			>>>divmod(7, 2)
			(3, 1)
			>>> divmod(8, 2)
			(4, 0)
			>>> divmod(1+2j,1+0.5j) （python2.3之后支持复数的处理）
			((1+0j), 1.5j)
	5. open(name[,mode[,buffering]]) -- 打开文件，返回file对象
	
		open的参数：
	         name -- 待打开文件的文件名字符串
		     mode -- 打开文件的模式（r--只读；rb--二进制形式打开只读；r+--读写方式打开；w--只写，内容覆盖；
		                           rb+ -- 二进制的读写；wb--二进制只写；w+--读写；wb+--二进制读写；
		                           a--只写，内容追加；ab--二进制写，追加；a+--读写，追加；ab+--二进制写，追加）
	         buffering -- 值为0：不会有寄存；
	                      值为1：寄存行；
	                      值大于1的整数：寄存区的缓冲大小；
	                      值小于0（负数）：寄存区缓冲大小为系统默认大小
	    file对象的方法：
			file.read([size]) -- size未指定则返回整个文件，size>2被内存报错
			file.readline() -- 返回一行
			file.readlines([size]) -- 返回包含size行的列表，size未指定返回全部行
			file.write(str) -- 写入字符串
			file.tell() -- 返回一个整数（到文件头的比特数），表示当前文件指针的位置
			file.seek(偏移量[,起始位置]) -- 用来移动文件指针
			                （偏移量单位为比特，可正可负；起始位置：0-文件头（默认），1-当前位置，2-文件尾）
			file.close() -- 关闭文件
	6. input(提示语) -- 接受标准输入（键盘输入）（接受合法的python表达式,可以接受一个python表达式输入，并将其运算输出结果）
						str = input("请输入：")
						print(str)
						如果输入：[i for i in range(5)]
						输出结果：[0,1,2,3,4]  
    7. raw_input(提示语) -- 接受任意类型输入（将所有输入当成字符串看待，eval(raw_input())等同于input()功能）,在python3中已经去掉了这个函数；

    8. classmethod()和staticmethod() -- 分别是类方法和静态方法的装饰器函数；
    9. all(iterable) -- 用于判断可迭代对象是否全为True，全为True返回True，否则返回False ；
    10. any(iterable) -- 用于判断可迭代对象时候全为False,全为False返回False,只要有一个为True则返回True；
    11. bool() -- int的子类，将参数转换成布尔类型（默认没有参数返回False）；
    12. chr() -- 用一个范围在0～255整数作参数，返回一个对应的字符，即当前整数对应的 ASCII字符
    13. ord() -- 以一个字符（长度为1的字符串）作为参数，返回对应的ASCII数值，或者 Unicode数值
    14. delattr(object, name) -- 删除object的属性name；
    15. cmp(x,y) -- 比较x和y的大小（如果x小于y,返回-1；如果等于返回0；如果大于返回1）
    16. dict() -- 不传参创建一个字典，传参将参数转换成字典；
    17. dir() -- 返回当前范围内的变量、方法和定义的类型列表，带参数时返回参数的属性方法列表；
    18. enumerate(sequence,[start=0]) -- 将一个可遍历的数据对象（列表、元祖或者字符串组合为一个索引序列，同时列出数据和数据下标，一般用在for循环当中）
    19. eval() -- 将传入的字符串当程序执行
    20. execfile(filename) -- 执行一个文件内的程序（可以加两个参数）
    21. filter(function,iterable) -- 通过function过滤iterable,返回符合条件的新列表
    22. float(参数) -- 将整数或者字符串转换成浮点数
    23. str.format(a,b) -- 格式化输出字符串，将str中{}中的变量用format参数替换掉
    24. frozenset(iterable) -- 返回一个冻结的集合（不能添加或删除任何元素）
    25. getattr(obj,name[,default]) -- 返回obj对象的name属性值，如果没有该属性，返回defaule默认值，没有默认值，也没有name属性会报错
    26. globals() -- 以字典形式返回当前位置全部全局变量
    27. locals()函数 -- 以字典类型返回当前位置全部局部变量
    28. hasattr(obj,name) -- 判断obj是否有name属性
    29. setattr(obj,name,value) -- 给obj属性name设置value值
    30. hash(obj) -- 获取obj的哈希值
    31. help(obj) -- 查看函数或模块用途的详细说明
    32. id(obj) -- 返回obj的内存地址
    33. issubclass(class1,class2) -- 判断class1是否是class2的子类
    34. iter(obj[,sentinel]) -- 将obj转成迭代器
    35. map(function,iterable1,iterable2...) -- 将iterable数据一一调用function，返回新列表
		>>> map(lambda x: x ** 2, [1, 2, 3, 4, 5])  # 使用 lambda 匿名函数
		[1, 4, 9, 16, 25]
		 
		# 提供了两个列表，对相同位置的列表数据进行相加
		>>> map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10])
		[3, 7, 11, 15, 19]
    36. next(iterable) -- 返回iterable的下一个对象
    37. reduce(function,iterable) -- 将iterable中的数据用function方法累积，function需要n个参数，将iterable前n个参数调用function返回结果作为参数再结合iterable剩下数据继续调用function，直到结束，返回结果
    38. reverse() -- 反向列表中的元素（list1.reverse()将list1元素倒序）
    39. sorted(iterable[,cmp[,key[,reverse]]]) -- 将iterable排序（默认升序）
    40. super() -- 返回父类（超类），如果是多继承，可以在super参数中传入想要调用的父类
    41. var([obj]) -- 返回obj的属性和属性值的字典，没有参数返回当前位置的属性和属性值 
    42. zip(iterable1,iterable2...) --  将每个iterable的对应的参数打包成一个元祖，返回这些元祖组成的列表，元素不一致，以最短的iterable为准返回相应列表，为减少内存，python3返回值是一个可迭代对象，要得到列表，用list转

# 四十一： python实现简单的socket通信
**epoll/poll/select能提高非阻塞式通信效率，windows上只有select**
## 1. 阻塞式通信：
	服务器端：
	import socket
	server = socket.socket() # 创建套接字对象
	server.bind(('10.7.187.61',8080)) # 绑定端口
	server.listen(100) # 监听服务
	while True:
	   conversation,address = server.accept() # 接受客户端请求，建立会话并和请求地址一并返回
	   cli_data = conversation.recv(1024) # 接受并缓存客户端发送的二进制数据
	   message = input('输入发送到客户端的数据：')
	   conversation.send(message.encode(encoding='utf-8')) # 向客户端发送二进制数据
	   # conversation.close()

	客户端：
	import socket
	client = socket.socket() # 创建客户端对象
	client.connect(('10.7.1187.61',8080)) # 连接服务端
	while True:  # 一直开启客户端
	   n = input('向服务端发送消息：') 
	   client.send(n.encode('utf-8')) # 向服务端发送消息
	   server_data = client.recv(1024)  # 缓存并接受服务端发送的消息 
## 2. 非阻塞式通信：
	服务器端（客户端类似阻塞式）：
	import socket
	server = socket.socket()
	server.setblocking(False)  # 设置非阻塞式通信
	server.bind(('10.7.168.61', 8000))
	server.listen(100)
	cli_con = []
	while True:
	   try:
	      conversation,addr = server.accept()  # 需要有客户端连接，如果没有连接，会报BlockingIOError错
	      cli_con.append((conversation,addr))
	   except:
	      pass
	   for conversation,addr in cli_con:
	      try:
	        client_recv = conversation.recv(1024)
	        if client_recv:
	           print(f'客户端信息：{client_recv}')
	           message = input('输入信息：回应客户端：')
	           conversation.send(message.encode(encoding='utf8'))
	        else:
	            client_recv.close()
	            cli_con.remove((conversation,addr))
	      except:
	        pass

# 四十： django异步请求框架：celery


# 三十九： 发布系统设计
# 三十八： 系统定时任务：crontab -e 
### a. 概论
	linux系统是由crond系统服务来控制的，原本就有很多计划性工作，因此这个系统服务是默认
	启动的，也为使用者提供了计划任务的命令： crontab 命令；
	
	crond是linux下周期性执行任务的一个守护进程，与windows下的计划任务类似，当安装完成
	操作系统后默认会安装此服务，并且会自动启动crond进程，该进程会定期检查是否有要执行的
	任务，如果有，则自动执行；
### b. linux下两种任务调度方式 -- 系统任务调度和用户任务调度；
**无论是那种方式，调度任务配置文件中每一行就可以对应配置一个调度任务**

	系统任务调度 -- /etc/crontab文件中配置调度任务，只有root用户能用
	比如写缓存数据到硬盘、日志清理等。在/etc目录下有一个crontab文件，就是系统任务调度配置文件；
	
	用户调度任务 -- crontab -e命令，所有用户都能用，任务自动写入/var/spool/cron/username中
	用户自定义自己的调度任务；
	
		crontab [-u uaername] [-l/-e/-r] -- 
			-u  ： 只有root能使用该选项，为指定的用户创建/移出crontab任务；
			-e  : 编辑crontab任务(创建或者移出)
			-l  ：查看crontab任务
			-r  ：清空当前用户所有的crontab任务（移出某个任务，用-e）

### c. 语法格式
	crontab定时任务每项工作 (每行)的命令格式有六个栏位，前五个都是时间，最后一个是命令：
		第一个栏位： 代表分钟（0-59或者*）
		第二个栏位： 代表小时（0-23或者*）
		第三个栏位： 代表日期（1-31或者*）
		第四个栏位： 代表月份（1-12或者*）
		第五个栏位： 代表星期（0-7或者*，其中0和7都代表星期天）
		第六个栏位： 代表任务命令
	
		前五个栏位的辅助字符：
		    *（星号） -- 代表任何时刻
		   ，（逗号） -- 代表分割时段的意思（多个时刻）
		    -（减号） -- 代表一段时间范围内
		    /(斜线) -- 代表每隔单位时间间隔
	
		以下几个crontab定时任务：
				0 3,6 * * * command   -- 3：00和6：00执行command
				20 8-12 * * * command  -- 8点到12点之间的每小时20分斗进行command
				*/5 * * * * command  -- 没五分钟进行一次command（0-59/5 * * * * command）
	    注意： 日月和周循环不能同时出现，系统可能会错误的执行
# 三十七： python是如何寻找包的,如何执行linux命令？
**python内置的sys模块可以与python运行时的配置或资源交互，调用相关函数或变量，比如python解释器，os模块能实现基本的操作系统函数/变量功能，可以通过dir(os)/dir(sys)查看模块中的方法或变量**
### 1. sys模块 ：
	sys.argv -- 获取命令行参数，第一个元素是程序本身路径，比如：['G:/wordspace/i18n/excel.py', 'runserver']
	sys.modules.keys() -- 返回所有已经导入的模块列表 
	sys.builtin_module_names -- Python解释器导入的模块列表
	sys.path -- 返回模块的搜索路径，初始化时使用PYTHONPATH环境变量的值
### 2. os模块 ： 
	os.sep -- 可以取代操作系统特定的路径分隔符，比如windows下为'\\\'；
	os.name -- 获取你正在使用的系统平台，‘nt’代表windows,'posix'代表linux/unix；
	os.getcwd() -- 返回当前python脚本工作的目录路径；
	os.getenv() -- 获取一个环境变量，如果没有则返回none;
	os.putenv(key,value) -- 设置一个环境变量；
	os.listdir(path) -- 返回 path路径下所有文件和目录名（列表）；
	os.remove(path) -- 删除一个文件；
    os.rename(oldname,newname) -- 重命名文件
	os.mkdir() -- 创建目录
	os.makedirs() -- 创建多层目录
	os.rmdir()/removedirs() -- 删除目录/多层目录
	os.chmod() -- 改变目录权限
	os.pardir -- 获取当前目录的父目录
	os.stat('path/filename') -- 获取目录/文件信息
	os.utime() -- 修改时间属性
    os.walk() -- 生成目录树下的所有文件名（返回对象）
	os.system(command) -- 运行shell命令（linux等）；
	os.linesep -- 获取当前平台使用的行终止符，windows使用‘\r\n’,linux使用‘\n’，Mac使用‘\r’;
	os.curdir -- 获取当前目录；
	os.chdir(dirname) -- 改变工作目录到dirname路径；
	
	os.path的相关用法：
		os.path.isfile(path) --  判断是否是文件，是文件返回True,是目录返回False
		os.path.isdir(path) -- 判断是否是目录,是目录返回True,是文件返回False
		os.path.exists(path) -- 判断path是否有效
		os.path.getsize(path) -- 返回文件大小，如果是目录返回OL
		os.path.abspath(__file__) -- 返回绝对路径
		os.path.normpath(path) -- 返回path的标准规范格式 
		os.path.split(path) -- 将path分割成目录和文件名，返回元祖
		os.path.splittext() -- 分离文件名和扩展名
		os.path.join(path,name) -- 将目录path和文件名name用‘\’连接
		os.path.basename(__file__) -- 返回当前文件的文件名
		os.path.dirname(__file__) -- 返回当前文件上级目录
		os.path.getatime(path) -- 返回path所指向的文件或者目录的最后存取时间
		os.path.getmtime(path) -- 返回path所指向的文件或者目录的最后修改时间
        os.environ -- 获取系统环境变量
其中： \_\_file\__是当前工作环境的文件路径
# 三十六： 2，8，10，16进制数之间的转换：
### 1. 将任意进制数转换为2进制数： bin() --
      bin(10)  -->  0b1010
### 2. 将任意进制数转换为10进制数： int() --
      int('10', 10) -- > 10 # 将传入的字符串当10进制数转换成10进制数
      int('10', 2) --> 2 # 将传入的字符串当2进制数转换成10进制数
      int('1010',2) --> 10 # 将传入的字符串当2进制数转换成10进制数
      int('1010') --> 1010 # 默认将传入的字符串当10进制转换成10进制数
### 3. 将任意进制数转换成8进制数： oct() --
      oct(1010) --> 0o1762
### 4. 将任意进制数转换成16进制数：  hex() --
      hex(10) -- > 0xa
# 三十五： python内置模块： collections
**from collections import nametuple,deque,defaultdict,OrderedDict,Counter 不止这五种方法，还有其他collections内置的方法**
### 1. nametuple -- 命名元祖
**命名元组有助于对元组每个位置赋予意义，并且让我们的代码有更好的可读性和自文档性**
		Point = namedtuple('Point', ['x', 'y'])  # 定义命名元组
		p = Point(10, y=20)  # 创建一个元祖对象 Point(x=10,y=20)
		a = p.x + p.y
		print(a)  # 结果：30
### 2. deque -- 双端队列
**双向队列对象，Deque队列是由栈或者queue队列生成的（发音是 “deck”，”double-ended queue”的简称）。Deque 支持线程安全，内存高效添加(append)和弹出(pop)，从两端都可以，两个方向的大概开销都是 O(1) 复杂度**

### 3. defaultdict -- 内建dict类的子类，它覆写了一个方法并添加了一个可写的实例变量（比使用dict.setdefault 方法快）
**可以设置字典value的默认数据类型，一般设置为容器类，比如，list,tuple,dict等，如果key对应的值没有，会创建对应的空容器**
		s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
		d = defaultdict(list)  # 设置字典d的value默认是列表
		for k,v in s:
		   d[k].append(v)
		r_list = [(i, sum(dict(d)[i])) for i in dict(d)]
		print(r_list)   # 输出结果： [('yellow', 4), ('blue', 6), ('red', 1)]

### 4. OrderedDict -- 有序字典
### 5. Counter -- 计数器
**Counter是dict的一个子类，因此具有dict的属性与方法。如常用的iteritems, items, get, pop**

	    将一个容器类数据传入Counter()，返回一个Counter对象
	    a. 计数器对象的elements()方法： 
	      返回一个生成器，可以通过elements方法创建重复元素（无序的）
		  c = Counter(a=4, b=2, c=0, d=-2)
		  a = list(c.elements())  # ['a', 'a', 'a', 'a', 'b', 'b'],这个序列生成出来是无序的（在转为列表之前）
	    b. 计数器对象的most_common()方法（根据计数降序排列）： 
	       返回一个列表，列表的元素是元祖，元祖第一个元素是特征值，第二个元素是统计的次数，如：[('action', 2), ('love', 1)]，默认返回所有特征值，当传入int参数n时，返回前n个参数
	    c. 计数器对象的update()方法：
	       根据参数，增加key的计数，无论输入输出，value的值都可以是负数
	    d. 计数器对象的substract()方法：
	       与update相反，根据参数，减少key的计数，无论输入输出，value的值都可以是负数
			c = Counter(a=4, b=2, c=0, d=-2)
			d = Counter(a=1, b=2, c=3, d=4)
			c.subtract(d)   # c : Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})
	    e.计数器对象的copy()方法：
	       返回对象的一个浅拷贝
	    f. 支持运算符（+、—、&、|）：
			c = Counter(a=3, b=1)
			d = Counter(a=1, b=2)
			c + d   # 结果： Counter({'a': 4, 'b': 3})
	        c & d   # 结果： Counter({'a': 1, 'b': 1}) ，相同特征key值，取统计数小的值
	        c | d   # 结果： Counter({'a': 3, 'b': 2}) ，相同特征key值，取统计数大的值
# 三十四： 数据库三范式、五大约束 -- 
### 1. 三大范式：
		第一范式（1NF）：数据表中的每一列必须是不可拆分的最小单元，确保每一列的原子性
		第二范式（2NF）：满足1NF后，要求表中的所有列，都必须依赖于主键，不能有任何一列与主键没关系，一个表只描述一件事
		第三范式（3NF）：必须满足第二范式，要求表中的每一列只与主键直接相关而不是间接相关
### 2. 五大约束：
		primary key : 主键约束
		unique : 唯一性约束
		default : 默认值约束
		not null : 非空约束
		foreign key : 外键约束
# 三十三： django项目国际化: i18n -- 
**18表示Internationalization这个单词首字母I和结尾字母N之间的字母有18个**

	涉及到的包：
	from django.utils import translation
	from django.utils.translation import ugettext as _
### 1. 安装工具包： pip install gettext,需要注意的是，linux或者苹果系统下可以直接安装，windows系统下安装不成功的话，需要先下载另外一个工具：https://mlocati.github.io/articles/gettext-iconv-windows.html?tdsourcetag=s_pcqq_aiomsg，安装该工具后再安装gettext；

### 2. 在settings中配置存放语言转换的文件夹路径：
	LOCALE_PATHS = (
	    os.path.join(BASE_DIR, 'locale'),
	)
### 3. 在代码中将需要转换的语句通过ugettext转换
		from django.shortcuts import render
		from django.http import HttpResponse
		from django.utils import translation
		from django.utils.translation import ugettext as _
		
		
		def test(request):
		    user_language = request.GET.get('lang_code', 'en')  # 接受url的参数，设置语音
		    translation.activate(user_language)  # 将全局语言设置为user_language
		    output = _('hello my world!')
		    return HttpResponse(output)
        其中：
        后端将变量或者字符串语言类型转换： output = _('hello my world!')

        前端转换，需要在第一行加入load i18n：
		{% load i18n %}
		
		<!DOCTYPE html>
		<html lang="en">
		<head>
		    <meta charset="UTF-8">
		    <title>internationalization</title>
		</head>
		<body>
		       <!--第一种(推荐使用)-->
		       <div>{% blocktrans %}hello world!{% endblocktrans %}</div>
		       <!--第二种-->
		       <div>{% trans "ohell" %}</div>
		       <div>{{ data }}</div>
		</body>
		</html>
### 4. 生成语言转换文件：
    虚拟环境下输入命令： python manage.py makemessages -l zh_hans
    其中： zh_hans代表简体中文，ja代表日文，en代表英文等等
### 5. 在生成的语言文件夹下修改需要转换的语句：
    修改django.po文件中的msgstr，即将msgid的内容翻译成对应的语言，放在msgstr中
    其他代码不要动，如果在下面代码段中有出现  #fuzzy 说明有重复、模糊的翻译，

			#: .\internationlization\views.py:17
			msgid "i am back to forward"
			msgstr "私は後から前へ"
			
			#: .\templates\test.html:10
			msgid "hello world!"
			msgstr "ただいま"
			
			#: .\templates\test.html:11
			msgid "ohell"
			msgstr "ただ"
### 6. 如果修改了项目代码中需要转换的词语，需要再次生成语言文件进行更新替换：
     python manage.py makemessages

### 7. 修改语言文件后，再生成代码的编译文件django.mo：
    python manage.py compilemessages
    这个命令生成的是项目程序会编译的代码程序，不能随意更改

    
# 三十二： 多进程和多线程

### 1. 多进程 -- from multiprocessing import Process
    a. 方法一. 使用Process类创建进程对象：

        ps = Process(target=worker,name="worker",args=(a,))  # 创建进程对象
        ps.start()   # 激活进程
        ps.join()   # 阻塞进程

        其中，Process类的常用属性和方法如下：
		Process常用属性与方法：
            target:进程执行的方法或者说实现的功能的封装（需要传一个函数名）
		    name:进程名
		    pid：进程id
            args:给target方法传的参数
		    run()，自定义子类时覆写
		    start()，开启进程
		    join(timeout=None)，阻塞进程
		    terminate(),终止进程
		    is_alive()，判断进程是否存活
    b. 方法二. 创建Process类的子类，重写run()方法，即将要执行的功能放在run()函数里，
               再创建自定义进程的进程对象：

		class MyProcess(Process):
		    def __init__(self):
		        Process.__init__(self)  
		        # 此处还可以自定义声明子线程对象属性，在run中调用，实现给线程传参
		    def run(self):
		        print("子进程开始>>> pid={0},ppid={1}".format(os.getpid(), os.getppid()))
		        time.sleep(2)
		        print("子进程终止>>> pid={}".format(os.getpid()))
        myp = MyProcess()
        myp.start()

    c. 方法三. 使用进程池Pool -- from multiprocessing import Pool

		import os,time
		from multiprocessing import Pool
		 
		def worker(arg):
		    print("子进程开始执行>>> pid={},ppid={},编号{}".format(os.getpid(),os.getppid(),arg))
		    time.sleep(0.5)
		    print("子进程终止>>> pid={},ppid={},编号{}".format(os.getpid(),os.getppid(),arg))
		 
		def main():
		    print("主进程开始执行>>> pid={}".format(os.getpid()))
		    ps=Pool(5)
		    for i in range(10):
		        # ps.apply(worker,args=(i,))          # 同步执行
		        ps.apply_async(worker,args=(i,))  # 异步执行
		 
		    # 关闭进程池，停止接受其它进程
		    ps.close()
		    # 阻塞进程
		    ps.join()
		    print("主进程终止")
		 
		if __name__ == '__main__':
		    main()
    d. 方法四. os.fork() -- 只在liunx系统下有效，windows无效

		import os
		
		pid = os.fork()
		
		if pid == 0:
		    print("执行子进程，子进程pid={pid},父进程ppid={ppid}".format(pid=os.getpid(), ppid=os.getppid()))
		else:
		    print("执行父进程，子进程pid={pid},父进程ppid={ppid}".format(pid=pid, ppid=os.getpid()))

### 2. 多线程 -- from threading import Thread
     a. 方法一. 使用Thread类，创建线程对象 
        t1=Thread(target=download,args=('举起手来',))
		t2=Thread(target=download,args=('毒液',))
       其中，target是线程要执行的函数功能，args是给target函数传的参数
     b. 方法二. 创建Thread类的子类，重写run方法，即将要在子线程中实现的功能放在run()中
               如果要给线程对象传参，可以在子类init初始化中继承Treading属性后再添加自定义声明的
               对象属性，再创建子类的对象

			from threading import Thread
			import time,datetime,random
			class MyThread(Thread):
			    def __init__(self,film):
			        super().__init__()
			        self.film = film   # 自定义对象属性，实现给子线程传参
			    def run(self):
			        print('下载电影：%s' % self.film)
			        a=random.randint(3, 7)
			        print('耗时：%s' % a)
			        time.sleep(a)
			        print('%s下载结束' % self.film)
			t1 = MyThread('毒液')
			t2 = MyThread('金刚')
			time1= time.time()
			t1.start()
			t2.start()
			t1.join()  #  t1 结束后才执行后面的代码
			t2.join()  #  t2 结束后才执行后面的代码
			time2 = time.time()
			print(time2-time1)
### 3. 进程间的通信问题 (Queue/Pipe/Manager/Lock)--
**不同进程间内存不共享，进程间数据交互主要是队列和管道，数据共享是Manager（Lock数据安全锁）** 
#### a. Queue（子进程间的通信队列--先进先出） : 
	from multiprocessing import Queue，Process
	def f(test):
	    test.put('22')
	
	q = Queue() # 父进程中创建消息队列
	q.put('11')
	p=Process(target=f,args=(q,)) # 创建子进程
	p.start()
	p.join()
	print("取到："，q.get_nowait()) # 先拿到11
	print("取到:",q.get_nowwait())  # 后拿到22 （先进先出）

#### b. Pipe（主进程与子进程，或者子进程与子进程之间的通信管道）
	from multiprocessing import Process,Pipe
	def f(conn):
	    conn.send('11') # 发送消息
	    print("from parent:",conn.recv()) # 打印接收的消息
	    conn.close()
	
	parent_conn,child_conn = Pipe() # 生成管道实列，一个父进程端，一个子进程端，可以相互sendhe recv
	p = Process(target=f, args=(child_conn,))
	p.start()
	print(parent_conn.recv())  # 接收子进程发送的消息
	parent_conn.send('44')  # 向子进程发送消息
	p.join()

#### c. Manager（数据共享）
**Manager支持进程中数据共享，也支持其他很多操作，如Condition,Lock,Namesapce,Queue,RLock（递归锁）,Semaphore等**

	from multiprocessing import Process,Manager
	import os
	def f(d, l,lock):
	    lock.acquire()  # 加锁
	    d[os.getpid()] =os.getpid()
	    l.append(os.getpid())
	    print(l)
	    lock.release() # 释放锁
	with Manager() as manager:
	    d = manager.dict()  #生成一个字典，可在多个进程间共享和传递
	    l = manager.list(range(5))  #生成一个列表，可在多个进程间共享和传递
	    lock = Manager.Lock()
	    p_list = []
	    for i in range(2):
	        p = Process(target=f, args=(d, l，lock))
	        p.start()
	        p_list.append(p)
	    for res in p_list: #等待结果
	        res.join()
	    print(d)
	    print(l)
### 4. 线程安全 -- 多个线程对同一个数据进行操作（只是读取数据不存在线程安全）
**当多个线程同时对一个数据进行操作，一个线程将数据读出来处理后，但是还没有存进去，另外一个线程在此时去读取数据，这个时候就可能产生数据安全隐患，造成数据混乱问题**
##### 数据混乱安全问题解决方案： 加锁 -- Lock
		import threading,time
		class Account():
		    def __init__(self,balance,name):
		        self.balance = balance   # 余额
		        self.name = name
		        self.lock = threading.Lock()  ## 设置加锁对象属性
		    def save(self,num):
		        '''存钱'''
		        self.lock.acquire()    #  加锁
		        a=self.balance
		        time.sleep(8)
		        self.balance=a+num
		        self.lock.release()    #  解锁
		    def drw(self,num):
		        '''取钱'''
		        self.lock.acquire()    #  加锁
		        a=self.balance
		        time.sleep(8)
		        self.balance =a- num
		        self.lock.release()    #  解锁
		account1= Account(1000,'罗姝枭')
		t1 = threading.Thread(target=account1.save,args=(1000,))
		t2 = threading.Thread(target=account1.drw,args=(100,))
		t1.start()
		t2.start()
		t1.join()
		t2.join()
		print(account1.balance)

# 三十一： django框架model层中的Q/F函数
### 1. F() -- 将两个字段进行比较作为查询条件

       用F()方法实现查询物理成绩大于数学成绩的学生：
       stus = Student.objects.filter(physics__gt=F('math'))
       print(stu.s_name) 

       用普通的方法实现：
	    stus = Student.objects.all()
	    for stu in stus:
	        if stu.physics > stu.math:
	            print(stu.s_name)
### 2. Q() -- 与、或、非逻辑运算
        
       与运算： 查询年纪大于18且小于20的学生：
               stus = Student.objects.filter(s_age__gt=18, s_age__lt=20)
               stus = Student.object.filter(Q(s_age__gt=18) & Q(s_age__lt=20))
               stus = Student.objects.filter(Q(s_age__gt=18), Q(s_age__lt=20))
       或运算： 查询年纪 大于等于20或者小于等于16的学生
               stus = Student.objects.filter(Q(s_age__gte=20) | Q(s_age__lte=16))
       非运算： 查询小于20岁的学生信息 
               stus = Student.objects.filter(~Q(s_age__gte=24))