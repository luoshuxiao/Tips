# 七十一：线程池/进程池
# 七十：socketserver模块实现套接字并发通信
**该模块简化了编写网络服务器的任务**

# 六十九：WebSocket协议client、server长链接通信
**WebSocket是独立于http协议的,在单个TCP连接上进行全双工通信的协议,使得客户端和服务器之间的数据交换变得更加简单，允许服务端主动向客户端推送数据,在WebSocket API中，浏览器和服务器只需要完成一次握手，两者之间就直接可以创建持久性的连接，并进行双向数据传输**

### 1.产生背景：
	很多网站为了实现推送技术，所用的技术都是Ajax轮询，在特定的时间间隔，由浏览器主动对服务器
    发出http请求，然后由服务器返回最新的数据给客户端的浏览器，这种传统的模式带来明显的缺点，
    由于Ajax发送的请求也是http请求，无状态，即浏览器需要不断的向服务器发出请求，但http请求
    可能包含较长的头部，而真正有效的数据可能只是其中的一小部分，这样就会浪费很多的带宽资源；

	还有一种比较新的技术Comet也是做轮询,这种技术虽然可以双向通信，但是依然是需要反复发出请求，
    Comet中普遍采用的长链接也会消耗服务器资源。
    Comet的实现有两种方式：
    （1）基于Ajax的长轮询方式：浏览器发出http请求，服务器端接收到请求后，会阻塞请求直到有数
         据或者超时返回，浏览器JS处理请求的返回信息后再次发出请求，重新建立连接，在此期间服
         务器端可能已经有新的数据更新，服务器把数据保存，直到重新建立连接，浏览器会把所有数
         据一次性取回；
    （2）基于Iframe及htmlfile的流方式：html的标记iframe的src属性会保持对指定服务器的长链
        接请求，服务器可以不停的返回数据，相对于第一种方式，这种方式跟传统的服务器推则更接近

    所以，W3C在新一带HTML标准HTML5中提供了这种能实现浏览器和服务器间实现全双工通讯的网络技
    术WebSocket协议，能更好的节省服务器资源和带宽，更实时的进行通讯；因此，脚本不仅可以发起
    AJAX请求，还可以发起websocket请求，不同的是，ajax发送的是http请求。
### 2.WebSocket协议：
**WebSocket在建立连接之前会有一个Handshake(Opening Handshake)过程，在关闭连接前也有一个Handshake(Closing Handshake)过程，建立连接之后，两端即可进行全双工通信**

	websocket使用ws或者wss的统一资源标识符，类似HTTPS，其中wss表示在TLS上的websocket,比如：
		ws://example.com/wsapi
		wss://secure.example.com/
    websocket使用和http相同的tcp端口，可以绕过大多数防火墙的限制，默认情况下，websocket
    协议使用80端口；运行在TLS上，默认使用443端口；
一个典型的websocket建立连接的握手请求如下：

（1）Opening Handshake : 客户端发起连接Handshake请求（特殊的HTTP请求）

    客户端发起请求：
	    GET / HTTP/1.1
	    Host: server.example.com
	    Upgrade: websocket  
	    Connection: Upgrade
	    Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
	    Origin: http://example.com
	    Sec-WebSocket-Version: 13
    服务器的回应：
		HTTP/1.1 101 Switching Protocols
		Upgrade: websocket
		Connection: Upgrade
		Sec-WebSocket-Accept: fFBooB7FAkLlXgRSz0BT3v4hq5s=
		Sec-WebSocket-Location: ws://example.com/

	Upgrade -- 必须设置为websocket,表示这是一个特殊的HTTP请求，目的是将通信协议HTTP升级
               到websocket协议；
	Connection -- 必须设置Upgrade，表示客户端希望将连接升级；
    Sec-WebSocket-Keys  -- 是随机字符串，服务端会将此数据用来构造出一个SHA-1的信息摘要，
               把Sec-WebSocket-Key加上一个特殊的字符串“258EAFA5-E914-47DA-95CA-C5AB0DC85B11”，
               然后将结果SHA-1哈希，之后进行BASE-64编码，将结果作为“Sec-WebSocket-Accept” 头的值，
               返回给客户端，这样可以尽量避免普通http请求被误认为是websocket协议；
    Origin -- 可选的字段，通常用来表示浏览器发起此websocket连接所在的页面，类似Referer，但不同的是，
              Origin只包含协议和主机名；
    Sec-WebSocket-Version -- 支持的websocket版本，RFC6455要求使用的版本是13，之前草案的版本均应被弃用；
    HTTP/1.1 101 Switching Protocols -- 101是服务器返回的状态码，所有非101状态码都表示Handshake未完成；
    其他一些定义在 HTTP 协议中的字段，如 Cookie 等，也可以在websocket中使用；
（2）DATA Framing -- 数据的传输、封包
    websocket协议通过序列化的数据包传输数据，数据封包协议中定义了opcode（数据包类型，占4bits）/
    payload length(payload data长度，占7bits)/payload data(应用层数据)等字段
（3）Closing Handshake : 
    跟Opening Handshake相比，Closing Handshake简单很多，主动关闭的乙方发送一个关闭类型的数据包，对方收
    到后，再回复一个相同类型的数据包，关闭就完成了，关闭类型数据包遵守封包协议，Opcode为0x8,payload data可
    以携带相关的提示信息，如关闭的原因或者其他消息等；
### 3.WebSocket协议的优点：
##### （1）较少的控制开销 -- 
    在连接创建之后，服务器和客户端之间交换数据时，用于协议控制的数据包头部相对较小，在不包含
    扩展的情况下，对于服务器到客户端的内容，此头部大小只有2到10字节（跟数据包长度相关）；对于
    客户端到服务器的内容，此头部还需要加上额外的4字节的掩码。相对于HTTP请求每次都要携带完整的
    头部，此项开销显著减少了；
##### （2）跟好的实时性 -- 
	由于协议是全双工的，所以服务器可以随时主动给客户端发送数据，相对于HTTP请求需要等待客户端
    发送请求服务器才能响应数据，延迟更少，省掉了一个请求的时间；即使是和Comet等类似的长轮询比
    较，也能在短时间内传递更多次的数据；
##### （3）保持连接状态 -- 
	与http不同的是，websocket需要县创建连接，这是一种有状态的协议，通信时可以省去部分状态信
	息，但是http每个请求都可能携带状态信息，如身份认证等；
##### （4）更好的二进制支持 -- 
    websocket定义了二进制帧，相对于http可以更轻松地处理二进制内容；
##### （5）更好的压缩效果 -- 
    相对于http压缩，websocket在适当的扩展支持下，可以沿用之前内容的上下文，在传递类似数据时，
    可以显著地提高压缩率；
##### （6）可以支持扩展 -- 
    websocket定义了扩展，用户可以扩展协议，实现部分自定义的子协议，如部分浏览器支持压缩等；
### 4.数据的传输模式 -- 
**按照数据流的方向可分为三种传输模式：单工，半双工，全双工**
    单工通信（比如计算机和打印机）：
       指仅能单方向传输数据，通信双方中，一方固定为发送端，另一方固定为接收端，使用
       一根传输线，信号只能沿一个方向传输。
    半双工通信（比如早起的无线电对讲机）：
       允许两台设备之间双向数据传输，但是不能同时传输，当一端传输数据时，另外一段
       需要等数据传输完成之后才能传输，也就是说，一个时间段只能有一个方向的传输存
       在，但是可以双向传输；通信系统每一端的发送器和接收器，通过收、发开关转接到
       通信线上，进行方向的切换，因此，会产生时间的延迟，收发开福安实际上是软件控
       制的电子开关；
    全双工通信（比如大部分的网卡，电话，手机等）：
       允许两台设备同时进行双向资料传输，通信系统的每一端都设置了发送器和接收器，
       无需进行方向的切换，因此没有切换操作的时间延迟，对不能有时间延迟的交互应用
       十分有利（比如远程监测和控制系统），这种方式要求通讯双方均有发送器和接收器，
       同时需要两根数据线传送数据信号（可能还需要控制线和状态线，以及地线），全双工
       通信主要有两种形式，分别是时分双工和频分双工；

       时分双工（TDD,Time-Division Duplexing）,是指利用时间分隔多工技术来分隔传送
       及接收信号，它利用一个半双工的传输模拟全双工传输过程，时分双工在非对称网络（上传
       及下载带宽不平衡的网络）有明显的优点，它可以根据上传及下载的资粮量，动态的调整对
       应的带宽，如上传资料大量时，就提高上传的带宽，若资料量减少时在将带宽降低。另外一个
       优点是在缓慢移动的系统中，上传及下载的无线电路径大致相同，因此类似波束成型的技术可
       以运用在时分双工的系统中。以太网路，无线局域网（WLAN）、蓝牙等都可视为TDD；

       频分双工（FDD，Frequency Division Duplexing）,是利用频率分隔多工技术来分隔传送
       及接收的信号，上传及下载的区段之间用‘频率偏移’的方式分隔，若上传及下载的资料量相近时，
       频分双工比时分双工更有效率，在这个情形下，时分双工会在切换传送时，浪费一些带宽，延迟
       时间较长，而且线路较复杂，更耗电，频分双工另外一个好处是在无线电接收规划上较简单且有
       效率，因为一个设备传送及接收使用不同的频带，因此设备不会接收待自己传出的数据，传送及
       接收的数据也不会相互影响，在时分双工系统中，需要在邻近的区段中增加保护区段，但会使频
       谱效率下降，否则就要有同步机制，使一设备的传送和另一设备的接收同步，同步机制会增加系
       统的复杂度和成本，而且因为所有的设备及时间区块都要同步，也降低了带宽使用的灵活性。大
       部分的手机系统都是FDD；
### 5.websocket代码实现双向通信
**这里简单介绍客户端用javascript/python，服务器端用python写的websocket通信,其他语言实现的client、server网上都有资料**

	1. client端代码 (javascript版)：

		<!DOCTYPE HTML>
		<html>
		   <head>
		   <meta charset="utf-8">
		   <title>某某教程(runoob.com)</title>
		      <script type="text/javascript">
		         function WebSocketTest()
		         {
		            if ("WebSocket" in window)
		            {
		               alert("您的浏览器支持 WebSocket!");
		               // 打开一个 web socket
		               var ws = new WebSocket("ws://localhost:9998/echo");
		               ws.onopen = function()
		               {
		                  // Web Socket 已连接上，使用 send() 方法发送数据
		                  ws.send("发送数据");
		                  alert("数据发送中...");
		               };
		               ws.onmessage = function (evt) 
		               { 
		                  var received_msg = evt.data;
		                  alert("数据已接收...");
		               };
		               ws.onclose = function()
		               { 
		                  // 关闭 websocket
		                  alert("连接已关闭..."); 
		               };
		            }
		            else
		            {
		               // 浏览器不支持 WebSocket
		               alert("您的浏览器不支持 WebSocket!");
		            }
		         }
		      </script>
		   </head>
		   <body>
		      <div id="sse">
		         <a href="javascript:WebSocketTest()">运行 WebSocket</a>
		      </div>
		   </body>
		</html>

    2. client端代码 (python版)：

        import websocket

		def on_message(ws, message):  
            """服务器有数据推送时，可以处理推送过来的数据，然后send数据给服务器"""
            print(message)
		def on_error(ws, error): 
            """程序报错时，就会触发on_error事件,可以将错误信息写入日志等等"""
		    print(error)
		def on_close(ws):
            """连接关闭时触发on_close事件，可以将关闭时要处理的逻辑放着这个函数"""
		    print("Connection closed ……")
		def on_open(ws): 
            """连接到服务器之后就触发on_open事件，可以将连接成功处理的逻辑放在这"""
		    req = 'response data'
		    print(req)
		    ws.send(req)  # 向服务器发送数据
		if __name__ == '__main__':
			 websocket.enableTrace(True)  # 打开跟踪，查看日志
			 ws = websocket.WebSocketApp('ws://localhost:9998/echo',
			                                on_message=on_message,
			                                on_error=on_error,
			                                on_close=on_close)
			 ws.on_open = on_open
			 ws.run_forever(ping_timeout=40)  # ws启动后程序会一直挂在这里

	3. server端代码 （python版）：
	
		# pip install websocket-server
		from websocket_server import WebsocketServer
	    
		def new_client(client, server):
		"""新的客户端连接到websocket服务器时做的逻辑处理可以放到这个函数"""
		server.send_message_to_all('所有人注意啦，又有新伙伴加入我们了！')
		
		def message_received(client, server, message):
		"""接收客户端的消息，处理消息的逻辑可以放在这个函数"""
		print('客户端%s发来消息%s' % (client['id'], ,message))
		
		def client_left(client, server):
		"""当旧的客户端断开连接时的需要处理的业务逻辑可以放在这个函数"""
		print('客户端%s断开连接' % client['id'])
		
		if __name__ == '__main__':
			server = WebsocketServer(1002, '0.0.0.0')
			server.set_fn_new_client(new_client)
			server.ser_fn_client_left(client_left)
			server.set_fn_message_receivd(message_received)
			server.fun_forever()
