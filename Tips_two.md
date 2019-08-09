

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

# 四十： django异步请求框架：celery


# 三十九： 发布系统设计

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
**python字典3.6版本之后是有序的，之前版本是无序的**
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


# 三十一： django框架model层中的Q/F函数
### 1. F() -- 允许Django在未实际链接数据的情况下具有对数据库字段的值的引用，不用获取对象放在内存中再对字段进行操作，直接执行原生产sql语句操作

       用F()方法实现查询物理成绩大于数学成绩的学生：
       from django.db.models import F
       stus = Student.objects.filter(physics__gt=F('math'))
       print(stu.s_name) 

       用普通的方法实现：
	    stus = Student.objects.all()
	    for stu in stus:
	        if stu.physics > stu.math:
	            print(stu.s_name)

     通常情况下我们在更新数据时需要先从数据库里将原数据取出后方在内存里，然后编辑某些属性，最后提交；
        
		all = Student.objects.filter(auth="小明")
		for b in all:
		    math = b.math
		    b.math = math + 10
		    b.save
    
	使用F对象来计算：
        from django.db.models import Q
		Student.objects.filter(auth="小明").update(math=F("math")+10)

### 2. Q() -- 与、或、非逻辑运算
        
       与运算： 查询年纪大于18且小于20的学生：
               stus = Student.objects.filter(s_age__gt=18, s_age__lt=20)
               stus = Student.object.filter(Q(s_age__gt=18) & Q(s_age__lt=20))
               stus = Student.objects.filter(Q(s_age__gt=18), Q(s_age__lt=20))
       或运算： 查询年纪 大于等于20或者小于等于16的学生
               stus = Student.objects.filter(Q(s_age__gte=20) | Q(s_age__lte=16))
       非运算： 查询小于20岁的学生信息 
               stus = Student.objects.filter(~Q(s_age__gte=24))