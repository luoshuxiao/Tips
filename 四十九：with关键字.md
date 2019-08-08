#  python中的with关键字
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