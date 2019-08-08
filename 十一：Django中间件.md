# Django中间件：
**中间件是一个用来处理django的响应与请求的框架级别的钩子，它是一个轻量，低级别的插件系统，用于在全局范围内改变django的输入输出，每个中间件组件都负责做一些特定的功能**
### a. 如何自定义中间件：
	  1. 写一个中间件类，要继承MIDDLEWAREMIXIN类；
	  2. 重写父类中响应的中间件方法；
	  3. 将自定义的类名添加配置到setting.py文件的MIDDLEWARE配置中；
### b. 根据需求重写父类的对象方法：

中间件中可以定义五个方法：

##### (1)def process_request(self,request)  # 视图函数之前执行
       
         返回值可以是none也可以是httpresponse对象，返回none，就按照正常流程走，交给下个中间件处理，
         返回httpresponse对象，django将不执行后面的中间件，也不执行视图函数，直接执行当前中间件的process_response;
         有多个中间件会按照MIDDLEWARE中注册顺序依次执行；
##### (2)def process_view(self,request,view_func,*args,**kwargs)  # process_response之后，视图函数之前执行
         返回值None，就正常执行;
         返回response对象，不执行后面的process_view和视图，直接执行所有中间件的process_response;
         有多个中间件会按照MIDDLEWARE中注册顺序依次执行； 
##### (3)def process_template_response(self,request,response)  # 在视图函数之后，process_response之前执行
		触发条件 -- 只有视图函数return中有render方法才触发此方法，
		返回response对象；
        多个中间件时，按照注册的倒序执行，执行完所有的process_template_response方法后执行response.render方法
##### (4)def process_exception(self,request,exception)  # 在视图函数之后，process_response之前执行
        触发条件 -- 只有出现异常才会出发该方法；
		返回None，表示不对错误进行处理，交给下一个中间件处理；
		返回response对象，表示下一个中间件的process_exception不执行，直接执行所有中间件的process_response方法；
		多个中间件时，按照注册的倒序执行；
##### (5)def process_response(self,request,response) # 视图函数之后
          返回值必须是httpresponse对象（可以直接返回response），
          有多个中间件时，按照注册的倒序执行

### c. 使用场景：
	（1） 缓存 -- 中间件去缓存看看有没有数据，有直接返回，没有再执行业务逻辑；
	（2） IP限制 -- 阻止特定的IP访问，或者设置单位时间内访问url的次数；
	（3） url访问过滤 -- 项目中有些url需要登录才能访问，可以在中间件写登录状态校验
