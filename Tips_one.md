
# 二十九： MVC / MVT / MVP / MVVM
### 1. MVC -- Model Views Controller -- 模型层、模板层、视图函数
### 2. MVT -- Model Views Templates -- 模型层、视图函数、模板层 
### 3. MVP -- Model Views Presenter -- 模型层、模板层、视图函数（contrller/Presenter）
### 4. MVVM -- Model Views ViewsModel -- 模型层、模板层、视图函数
      将views和状态和抽象化，视图UI和业务逻辑分开，viewsmodel可以取出 Model 的数据同时帮忙处
      理 View 中由于需要展示内容而涉及的业务逻辑。
# 二十六：数据库删除操作（谨慎使用）：
        -- 删除数据库： drop database if exists 数据库名；
        -- 删除表：drop table 表名字 （完全删除去掉整张表）；
        -- 删除表：delete from 表名 （删除表里面的数据，一行一行的删除，表明后面可以跟where 字段名= 值，
                  删除指定的某条或者多条记录,该命令可以回滚）
        -- 删除表：truncate table 表名称 （删除表中的数据，并且新增加记录的计数标识会重置，
                  比如主键id原来是50，用该命令删除后，新增加的数据主键id会从1开始，而不是51开始）

       一般来说：执行速度-->drop>truncate>delete
       使用foreign key约束的表，不能用truncate，应使用不带where的delete

# 二十五 : GET和POST的区别：
**本质上来说，GET和POST请求都是TCP链接，TCP/IP都是HTTP的底层协议，它们两做的事情都是一样的，没有区别的，**
**但是由于HTTP协议或者浏览器、服务器对GET和POST的规定，让POST和GET不一样，这种不一样主要体现在以下三点：**

### 1. 请求参数传输方式不同： 
         GET请求的参数放在url中，安全性较低，参数完全暴露在外面，而POST请求的参数放在请求体中，
         安全性相比GET要好
### 2. 允许传递的参数大小不一样：
         GET将参数放在url中，数据量太大，对浏览器和服务器都是很大的负担，所以业界不成文的规
         定大部分浏览器都是限制在2k内，大部分服务器最多处理64k的url，而POST是放在请求体内，
         理论上来说参数大小是不受限的
### 3. GET产生一个TCP数据包，POST产生两个数据包：
         GET请求，浏览器会把HTTP的headers和data一并发出去，服务器返回数据，并响应200状态码；
         但是POST请求是，先发送headers,服务器响应100确认码，继续传输，浏览器再发送data，
         服务器响应数据和200状态码
    ps: 由于POST是两次传输数据，表面上看时间上会多于GET，但是据有关研究表明，在网络状态良好
        的状态下，这个时间差可以完全忽略掉，非常小，但是在网络差的环境下，POST方式可以更好
         的保证数据的完整性。


# 二十 ： 操作系统的五大管理功能 ：
	1.设备管路：主要是负责内核与外围设备的数据交互，实质是对硬件设备的管理，包括对输出输入设备的分配，初始化，维护与回收等，比如管理音频的输入输出；
	2.作业管理：这部分功能主要是负责人机交互，图形界面或者系统任务的管理；
	3.文件管理：这部分功能设计文件的逻辑组织和物理知识，目录结构和管理等；
    4.进程管理：说明一个进程存在的唯一标志是pcd（进程控制块），负责维护进程的信息和状态；
    5.存储管理：数据的存储方式和组织结构。

# 十八 ： SQL注入攻击 
 --> 用户在客户端输入特定的字符串提交服务器，在服务器执行sql语句时，将用户输入的特定字符串误以为是sql语句并且执行语句

如何防御sql注入攻击：

	1.项目上线时，将网页错误提示返回信息关闭，或者重写（python中配置：debug=False）,这种方法只是简单的掩盖代码缺陷，并不能防御;
	2.检查变量数据类型和格式；
	3.过过滤字符串；
	4.绑定变量，使用预编译语句；
	5.数据库信息加密；
    6.使用数据库存储过程；

# 十四： python容器类型（即数据类型）
## 1. 列表（list） --  可变，有序  --  中括号[]
		  a.获取元素 -  通过下标获取元素
		  b.增删改
		     增 ： append ,insert , extend
		     删除：remove , del ,pop ，clear
		     改 ： 列表[下标] =  新值
		  c. 相关运算 ：+ ，* ，in /not in ,len() ,list() ,max() ,min()

### 列表1.append（a） 和列表1.extend（a）的区别： 

          append: 添加对象到列表1（将添加的对象作为列表1的一个元素）
          extend: 添加元素到列表1（将添加的对象中的元素添加到列表1）
					a =  [1,2,3,4]      
					b =  [5,6,7,8]
					a.append(b)   # a: [1,2,3,4,[5,6,7,8]]
                    a =  [1,2,3,4] 
                    a.extend(b)  # a: [1,2,3,4,5,6,7,8]			

### 将[[1,2],[3,4],[5,6]]一行代码展开该列表,得出[1,2,3,4,5,6]
			a= [[1, 2], [3, 4], [5, 6]]
			b= [j for i in a for j in i]
## 2. 元祖（tuple） --  不可变，有序  --   小括号()
             注意： 当元祖只有一个元素时，要加逗号
                   a = (1)  ---   a变量类型是int类型
                   b = (1,)  ---  b变量类型是tuple类型

			  获取元素 -  通过下标获取元素
			              变量1，变量2 = （元素1，元素2）
			              变量1，*变量2 = （元素1，元素2，元素3......）
			  相关运算 ：+ ，* ，in /not in ,len() ,tuple() ,max() ,min()
## 3.  字典 （dict） --  可变，有序  --  大括号{}
			   a.获取元素  -- 通过键获取元素
			   b.增删改
			   增  ： 字典[key] = 值 ， 字典1.update（字典2）， 字典1.setdefault(key,值)
			   删  ：  del  字典[key]，字典.pop(key) ，clear
			   改  ：字典[key]  = 值
			   c. 相关运算 ：in /not in ,len() ,dict() ,
			          max() : 取的是字典的key的最小值 ,key类型需要一样
			          min() ：取的是字典的key的最小值 ,key类型需要一样
## 4. 集合 （set)  --  可变、无序  --大括号{}
              a. 查--获取集合元素 ： 不能单独获取某个元素，只能遍历
			  b. 增 （添加元素）： 集合.add(元素) --  将制定元素添加到集合中
			                  集合.update(序列) --  将序列中的元素添加到集合中（序列中的元素必须是不可变的）
			  c. 删 （删除元素）：  集合.remove(元素)   --  删除集合中指定的元素
			  d.   in / not in  ,max ,min, len ,set
              e.数学运算：包含（>=,<=）,并集（|）,交集（&），补集（^）,差集（-）

## 5. 字符串（str）-- 不可变、 有序--两个单引号''或者双引号
          a.获取元素  -- 通过下标获取元素
          b. 字符串切片：字符串1[:] 
          c. 相关运算 ：+ ，* ，in /not in ,len() ,str() ,max() ,min()
          d.转义字符：\n,\t,\',\
          e.阻止转义：r/R


# 八： 闭包问题  （变量作用域）
### 1. python属性查找规则：LEGB
		1. （Local）局部作用域，每当调用一个函数的时候就创建了一个局部作用域，它最先被搜索。 
		2. （Enclosing）嵌套的父级函数的局部作用域 
		3. （global）全局作用域 
		4. （built-in）内建作用域，这个是内建函数和类的作用域。

### 2.	 实列：
		1）	 def func(x):
		        a = []
		        for i in range(5):
		            a.append(i*x)
		        return a
		     b = func(2)
		     print(b)
       

        输出结果为：[0, 2, 4, 6, 8]

      2）
		def func():
		   return [lambda x : i * x for i in range(4)]
		
		print([m(2) for m in func()])
        
        输出结果为： [6, 6, 6, 6]
        如果想得到[0,2,4,6]可以用生成器或者创建闭包或者偏函数

        生成器
        def multipliers():
              for i in range(4): yield lambda x : i * x
        print([m(2) for m in multipliers()])

        将闭包作用域变为局部作用域
        def multipliers():
              return [lambda x，i=i : i * x for i in range(4)]
        print([m(2) for m in multipliers()])

        偏函数
		from functools import partial
		from operator import mul
		
		def multipliers():
		  return [partial(mul, i) for i in range(4)]
        print([m(2) for m in multipliers()])

# 七： 映射（map()） --  归纳（reduce()） -- 过滤（filter()） -- 
#   解析式生成可迭代对象:列表解析式，元祖解析式，字典解析式等（任何可迭代对象）

	1） map(函数，可迭代序列对象) -- 对可迭代对象的每个元素执行函数，返回一个序列对象（需要指定保存类型则：list(map())） <--> （数据处理）

	2) reduce(函数，可迭代对象) -- 通常map和reduce都是在列表里结合使用，map对数据进行一一映射处理，reduce对数据进行整合计算 <-->（数据整合）

	3） filter（函数，可迭代对象） --  将可迭代对象的元素中满足函数的保留下来，不满足的剔除掉 <-->（数据筛选）

	4） 解析式是python生成列表的一种高效方式（也可以生成其他类型，通常生成list） ： 列表解析式 -- [ function for item in iterable] 
	
	   比如 ： [ x * x for x in range(1,5)]
	          [ num * num for num in range(-8,5) if num < 0]

    字典解析式：
	# Taken from page 70 chapter 3 of Fluent Python by Luciano Ramalho
	
	DIAL_CODES = [
	    (86, 'China'),
	    (91, 'India'),
	    (1, 'United States'),
	    (62, 'Indonesia'),
	    (55, 'Brazil'),
	    (92, 'Pakistan'),
	    (880, 'Bangladesh'),
	    (234, 'Nigeria'),
	    (7, 'Russia'),
	    (81, 'Japan'),
	    ]
	
	>>> country_code = {country: code for code, country in DIAL_CODES}
	>>> country_code
	{'Brazil': 55, 'Indonesia': 62, 'Pakistan': 92, 'Russia': 7, 'China': 86, 'United States': 1, 'Japan': 81, 'India': 91, 'Nigeria': 234, 'Bangladesh': 880}
	>>> {code: country.upper() for country, code in country_code.items() if code < 66}
	{1: 'UNITED STATES', 7: 'RUSSIA', 62: 'INDONESIA', 55: 'BRAZIL'}

	集合解析式：
	
	# taken from page 87, chapter 3 of Fluent Python by Luciano Ramalho
	
	>>> from unicodedata import name
	>>> {chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i), '')}
	{'×', '¥', '°', '£', '', '#', '¬', '%', 'µ', '>', '¤', '±', '¶', '§', '<', '=', '', '$', '÷', '¢', '+'}

# 六: 分布式、高并发
# 五： 字符串格式化-- format函数 （菜鸟教程）

功能： a.代替占位符： f'{a}任意字符{b}' -- 等同于--> '%s任意字符%s' %(a,b)
      b.格式化字符串：'{a}{b}'.format(a='内容'，b='内容')

实列：

    1.传入参数：
	#!/usr/bin/python
	# -*- coding: UTF-8 -*-
	 
	print("网站名：{name}, 地址 {url}".format(name="菜鸟教程", url="www.runoob.com"))
	 
	# 通过字典设置参数
	site = {"name": "菜鸟教程", "url": "www.runoob.com"}
	print("网站名：{name}, 地址 {url}".format(**site))
	 
	# 通过列表索引设置参数
	my_list = ['菜鸟教程', 'www.runoob.com']
	print("网站名：{0[0]}, 地址 {0[1]}".format(my_list))  # "0" 是必须的

    2.传入对象
	#!/usr/bin/python
	# -*- coding: UTF-8 -*-
	 
	class AssignValue(object):
	    def __init__(self, value):
	        self.value = value
	my_value = AssignValue(6)
	print('value 为: {0.value}'.format(my_value))  # "0" 是可选的
    3.格式化数字：
	>>> print("{:.2f}".format(3.1415926));
	3.14

# 三：  装饰器：一个闭包，把一个函数当做参数返回 一个替代版的函数，本质上就是一个返回函数的函数 (被装饰的函数名会变成装饰器的名字，不在是原来的名字)

		装饰器的三个要素（）：
		 
		1. 外层函数嵌套内层函数
		2. 外层函数返回内层函数
		3. 内层函数调用外层函数参数
		
		#  对要装饰的函数添加新的代码
		def outer(func):
		    def inner(*args, **kwargs):
                    # 需要装饰的代码（在func基础上添加的新代码）
		            return func(*args, **kwargs)
		    return inner
# 二： 偏函数：把一个函数的某些参数固定住（设默认值），返回一个新的函数

    列子：

	int('234') -- 将'234'字符串变成int类型 --int('234', base=10)将字符串引号去掉后，当成10进制的数，然后转换成10进制数返回
	int('1010',base=2) -- 将字符串去掉引号后当成一个2进制数来算，转成10进制数返回
    
    自定义偏函数：

    导入偏函数模块：from functools import partial
    int2 = partial(int, base=2)
    int2就是一个偏函数 
       -- int2('101011')--将101011当2进制，转换成10进制数

# 一： 网络传输协议：

**OSI（open system interconnection）七层模型 、协议，由于OSI是一个理想的模型，因此一般网络系统只涉及其中的几层，很少有系统能够具有所有的7层，并完全遵循它的规定**

	第七层--应用层：各种应用程序协议，如HTTP/FTP/SMTP/POP3；
	第六层--表示层：信息的语法语义以及他们的关联，如数据格式化、加密、解密、转换翻译、压缩解压缩等；
	第五层--会话层：不同机器上的用户之间建立、管理会话；
	第四层--传输层：接受上一层的数据，提供端对端的接口，必要的时候进行分割，并将数据交给网络层，且保证
                   数据段有效到达；（TCP/UDP）
	第三层--网络层：控制子网的运行。为数据包选择路由，如逻辑编址，分组传输、路由选择等； 
	第二层--数据链路层：物理寻址，同时将原始比特流转变为逻辑传输线路
	第一层--物理层：机械、电子、定时接口通信信道上的原始比特流传输，以二进制数据形式在物理介质上传输数据


	   物理层：
			主要功能是利用传输介质为数据链路层提供物理连接，以实现相邻计算机节点之间比特流的透明传输（指比特
            流经实际电路传送前后无变化，不受电路影响，当电路透明不存在），尽可能屏蔽掉具体的传输介质和物理设备
            差异，让上层数据链路层不必考虑传输介质带来的影响。
	
	   数据链路层：
			由于计算机网路中存在各种干扰，物理链路不可靠，这一层在物理层提供的比特流基础上，负责建立和管理节点
            间链路，通过各种控制协议（差错控制，流量控制方法等）解决同一网络节点之间的通信，将有差异的物理信道
            变为无差错的，能可靠传输数据帧的数据链路，即提供可靠的通过物理介质传输数据的方法，通常分MAC/LLC两
            层。（局域网内）
	
	   网络层：
			OSI模型中最复杂的一层，通信子网最高的一层，通过路由选择算法为报文或分组选择最适当的路径，数据链路
            的数据在网络层被转换成数据包，通过路径选择、分组组合、进/出路由等控制，将信息从一个网路设备传到另
            一个网络设备，解决不同子网间的通信。（各局域网之间）
	   
	   传输层：
			上三层的主要功能数数据处理，传输层主要是数据通信，是通信子网和资源子网的接口和桥梁，可靠传输（TCP）
            在必要时对数据 进行分割，传输到网络层，确保数据正确无误的传输到网络层，目标设备在指定时间内没有确认
            收到，数据将被重发，而不可靠传输（UDP）则只负责发送，不确保目标设备是否收到。
	   
	   会话层：
			用户应用程序和网络之间的接口，通过远程地址（为用户设计的域名），建立、组织、协调两个会话进程之间的
            通信，对数据交换进行管理
	   
	   表示层 ：
			对应用层的数据进行解释，格式化，压缩和解压，加密和解密等
	
	   应用层：
			模型的最高层，直接向用户提供服务，是用户与网络以及应用程序和网络间的直接接口，使的用户能够与网络进
            行交互式联系，该层的应用程序实现用户请求的服务，应用层为用户提供：文件服务、目录服务、文件传输服
            务（FTP）、远程登录服务（Telnet）、电子邮件服务（E-mail）、打印服务、安全服务、网络管理服务、数据
            库服务等。上述的各种网络服务由该层的不同应用协议和程序完成，不同的网络操作系统之间在功能、界面、实
            现技术、对硬件的支持、安全可靠性以及具有的各种应用程序接口等各个方面的差异是很大的