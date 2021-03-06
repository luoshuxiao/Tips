# Session/Cookie/Token：
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