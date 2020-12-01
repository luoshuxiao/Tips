# 一： python是如何寻找包的,如何执行linux命令？
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

# 二：sys模块