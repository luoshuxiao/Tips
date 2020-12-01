# python常用内置函数
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