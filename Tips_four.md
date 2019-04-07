# 五十六： mysql主从配置
**linux系统下配置my.cnf文件，windows下配置my.ini**
### a. 配置master数据库：

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

### b.配置slave数据库

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

