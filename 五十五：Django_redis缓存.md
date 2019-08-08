#  Django_redis缓存
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