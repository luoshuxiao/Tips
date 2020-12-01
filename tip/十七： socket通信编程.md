# 一：socket基础编程：
**epoll/poll/select能提高非阻塞式通信效率，windows上只有select**
## 1. 阻塞式通信：
	服务器端：
	import socket
	server = socket.socket() # 创建套接字对象
	server.bind(('10.7.187.61',8080)) # 绑定端口
	server.listen(100) # 监听服务
	while True:
	   conversation,address = server.accept() # 接受客户端请求，建立会话并和请求地址一并返回
	   cli_data = conversation.recv(1024) # 接受并缓存客户端发送的二进制数据
	   message = input('输入发送到客户端的数据：')
	   conversation.send(message.encode(encoding='utf-8')) # 向客户端发送二进制数据
	   # conversation.close()

	客户端：
	import socket
	client = socket.socket() # 创建客户端对象
	client.connect(('10.7.1187.61',8080)) # 连接服务端
	while True:  # 一直开启客户端
	   n = input('向服务端发送消息：') 
	   client.send(n.encode('utf-8')) # 向服务端发送消息
	   server_data = client.recv(1024)  # 缓存并接受服务端发送的消息 
## 2. 非阻塞式通信：
	服务器端（客户端类似阻塞式）：
	import socket
	server = socket.socket()
	server.setblocking(False)  # 设置非阻塞式通信
	server.bind(('10.7.168.61', 8000))
	server.listen(100)
	cli_con = []
	while True:
	   try:
	      conversation,addr = server.accept()  # 需要有客户端连接，如果没有连接，会报BlockingIOError错
	      cli_con.append((conversation,addr))
	   except:
	      pass
	   for conversation,addr in cli_con:
	      try:
	        client_recv = conversation.recv(1024)
	        if client_recv:
	           print(f'客户端信息：{client_recv}')
	           message = input('输入信息：回应客户端：')
	           conversation.send(message.encode(encoding='utf8'))
	        else:
	            client_recv.close()
	            cli_con.remove((conversation,addr))
	      except:
	        pass

# 二：socketserver模块实现套接字并发通信
**该模块简化了编写网络socket服务器的任务**

# 三：数据粘包处理