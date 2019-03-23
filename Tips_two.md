# 四十三： python常用内置函数
# 四十二： python实现socket通信
# 四十一： 读写exel文件:xlrd/xlwt和openpyxl
# 四十： django异步请求框架：celery
# 三十九： 发布系统设计
# 三十八： 定时任务：crontab -e 
# 三十七： python是如何寻找包的,如何执行linux命令？
**python内置的os模块能实现基本的操作系统功能**

	os.sep -- 可以取代操作系统特定的路径分隔符，比如windows下为'\\\'；
	os.name -- 获取你正在使用的系统平台，‘nt’代表windows,'posix'代表linux/unix；
	os.getcwd() -- 返回当前python脚本工作的目录路径；
	os.getenv() -- 获取一个环境变量，如果没有则返回none;
	os.putenv(key,value) -- 设置一个环境变量；
	os.listdir(path) -- 返回 path路径下所有文件和目录名（列表）；
	os.remove(path) -- 删除一个文件；
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

        ps = Process(target=worker,name="worker",args=())  # 创建进程对象
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
### 3. 进程间的通信问题 -- 
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