# 多进程和多线程

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

### 5. GIL（全局解释器锁）对python多线程性能的影响：
**某种情况下（线程串行）上来说会降低python性能**

	GIL是Python为了保证线程安全而采取的让线程独立运行的限制,一个核只能在同一时间运行
    一个线程，也就是说同一进程中假如有多个线程，一个线程在运行python程序时会霸占python
    解释器（GIL锁的功能），使该进程内的其他线程无法运行，如果线程运行过程中遇到耗时操
    作，则解释器锁解开，使其他线程运行，所以在多线程中，线程的运行仍是有先后顺序的，并
    不是同时进行；

    多线程优缺点：
	对于io密集型任务，python的多线程起到作用，但对于cpu密集型任务，python的多线程几
    乎占不到任何优势，还有可能因为争夺资源而变慢；

	多进程优缺点：
	解决办法就是多进程和协程(协程也只是单CPU,但是能减小切换代价提升性能)，多进程中因为
    每个进程都能被系统分配资源，相当于每个进程有了一个python解释器，所以多进程可以实现
    多个进程的同时运行，缺点是进程系统资源开销大。