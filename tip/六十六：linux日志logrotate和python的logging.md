# 一： linux日志文件总管 -- logrotate（自动备份/轮询日志输出文件）
**logrotate可以自动对日志进行截断（或轮循）、压缩以及删除旧的日志文件，旧日志也可以通过电子邮件发送**
## 1. 创建 配置文件 -- touch /etc/logrotate.d/super_log
和大多数linux工具的配置文件一样，logrotate的配置文件是/etc/logrotate.conf，通常不需要对它进行修改。日志文件的轮循通常设置在独立的配置文件中，放在/etc/logrotate.d/目录下
## 2. 编辑 配置文件 -- vim /etc/logrotate.d/super_log
		/var/log/supervisor/super_log*.log {
		    daily
		    rotate 30  # num of backups
		    dateext
		    dateyesterday # 用昨天的日期做后缀
		    copytruncate
		    delaycompress    # today and yesterday will not compress
		    compress
		    missingok
		    notifempty
		}
    daily: 日志按天轮询。也可以设置为weekly/monthly/yearly；
	rotate: 备份文件个数，超过的会删除；
	dateext: 备份文件名包含日期信息；
	dateyesterday: 用昨天的日期做后缀,日志一般是凌晨备份前一天的数据，如果不用这个参数，日志文件显示的日期和实际不是一天；
	copytruncate: 首先将目标文件复制一份，然后再做截取（防止直接将原目标文件重命名引起的问题）；
	delaycompress ：与compress选项一起用，delaycompress选项指示logrotate不将最近的归档压缩，压缩将在下一次轮循周期进行 就是最新两个日志文档不压缩；
	compress： 压缩文件。如果不想压缩 可以和delaycompress 一起去掉；
	missingok： 忽略错误；
	notifempty： 如果没有日志 不进行轮询；
    还有其他参数，如（size/postrotate/endscript等）；
## 3. 测试是否配置成功 -- 
     logrotate /etc/logrotate.conf -- 调用logrotate.d下配置的所有日志配置文件
     logrotate /etc/logrotate.d/super_log -- 调用配置的单个日志配置文件
     logrotate -vf /etc/logrotate.d/super_log -- 即使轮循条件没有满足，也可以通过使用-f选项来强制logrotate轮循日志文件，-v参数提供了详细的输出
## 4. 简单用列： 与supervisor结合使用 --
**supervisor用于进程的管理，自带有日志的配置项，但是只能以文件大小来作为轮询条件，当需要用时间来作为轮询条件时，可以借助logrotate工具，比如每天/每周轮询等，需要注意的是，用logrotate配置轮询时，supervisor自带的轮询配置要关闭,比如以下配置：**

        supervisor的配置：
			# /etc/supervisor/conf.d/my_app.conf
			[program:my_app]
			directory=/opt/%(program_name)s
			command=/opt/%(program_name)s/run
			
			stderr_logfile=/var/log/supervisor/%(program_name)s_stderr.log
			stdout_logfile=/var/log/supervisor/%(program_name)s_stdout.log
			
			# 不设置日志文件大小（设置为0）
			stdout_logfile_maxbytes=0
			stderr_logfile_maxbytes=0
			
			# 不设置备份文件个数（设置为0）
			stdout_logfile_backups=0
			stderr_logfile_backups=0

        logrotate的配置：
			# /etc/logrotate.d/my_app
			/var/log/supervisor/my_app_*.log {
			    daily
			    rotate 30  # num of backups
			    copytruncate
			    delaycompress    # today and yesterday will not compress
			    compress
			    missingok
			    notifempty
			}
# 二：logging模块
