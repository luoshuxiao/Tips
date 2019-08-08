#  mysql主从配置
**linux系统下配置my.cnf文件，windows下配置my.ini**

**mysql数据主从的复制是sql语句的复制，并不是真正意义上的数据复制，整个复制过程就是Slave从Master端获取bin-log日志然后在Slave中顺序的执行日志中所记录的sql操作**
### a. 主从的配置形式：
		一主一从
		主主复制
		一主多从 -- 可以增强系统读取的性能（读写分离）
		多主一从 -- 5.7版本开始支持
		联级复制

     配置主从的作用：
		实时灾备： 用于故障切换
		读写分离： 提供高效的查询服务
		备份： 避免宕机影响业务
     配置主从的必要条件：
	     主库开启binlog日志（设置log-bin参数）
	     主从server-id不同
	     从库服务器能连接上主库 
### b. 主从数据复制的原理：

	（1）主库生成一个binary log dump线程 -- 
	当从库节点连接主库节点时，主库会创建一个log dump线程，用于发送bin-log的内容，
    在读取bin-log的操作时，此线程会对主库上的bin-log加锁，当读取完成，发送给从节
    点之前锁会被释放；
	
	（2）从库生成一个I/O线程 -- 
	当从库节点上执行start slave命令后，从库会创建一个I/O线程用来连接主节点，请求
    主库中更新的bin-log.I/O线程接受到主库bin-log dump线程发送的更新之后，保存
    在本地的relay-log中；
	
	（3）从库SQL线程 -- 
	SQL 线程负责读取relay log 中的内容，检测到relay-log中新增了内容后，会解析成
    在主库中实际执行过的的操作并且执行，最终保证主从数据的一致性。

### c. mysql主从复制模式
**默认是异步模式，mysql增删改操作会全部记录在binary log中，当slave节点连接在master时，会主动从master处获取最新的bin log文件，并在从库解析、执行**

	（1） 异步模式 -- 主库不主动push bin log 到从节点（从库可能没
	                 有即时解析、执行最新的bin log）
	（2） 半同步模式 -- 主库收到一台从库返回的信息就会commit;
	（3） 全同步模式 -- 主从库都执行了commit并确认才会向客户端返回成功;
### d. 具体的主从配置实列（一主一从）
    (1)配置master数据库：

	编辑配置文件： vim /etc/my.cnf
	
	server-id = 200 # 设置主服务器的ID
	innodb_flush_log_at_trx_commit=2  # 操作系统崩溃或者低筒断电上一秒所有事务数据才可能丢失
	sync_binlog=1 # 开启binlog日志同步功能
	log-bin=mysql-bin-200 # binlog日志文件名
	binlog-do-db= 'database' # 这个表示只同步database数据库（没有这个配置表示同步所有）
	
	配置完成过后，重启mysql服务 ：  service mysql restart

	登录数据库：  mysql -uroot -p123456

	给slave数据库开通账号密码：
	grant replication slave on . to 'mark'@'192.168.1.201' identified by '123456' # 授权给从数据库服务器192.168.1.201，用户名mark,密码123456

	查看主库状态：
	show master status;     # slave数据库连接master数据库时有两个参数需要和File、Position一致

    (2)配置slave数据库

		编辑配置文件：  vim /etc/my.cnf
		
		server-id=201
		innodb_flush_log_at_trx_commit=2
		sync_binlog=1
		log-bin=mysql-bin-201
		
		配置完成后，重启mysql服务 ： service mysql restart
		
		登录mysql： mysql -uroot -p123456
		
		连接主数据库（master_log_file和master_log_pos分别是master中status中的File和Positon）： 
		 
		change master to master_host='192.168.1.200',master_user='mark' ,master_password='123456',master_log_file='mysql-bin-200.000002' ,master_log_pos=1167；
		
		开启从库： start slave;   (关闭从库： stop slave)
		
		查看从库状态： show slave status;
		
		如果slave_io_running和slave_sql_running 都是yes表示配置成功