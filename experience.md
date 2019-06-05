## 启动docker容器：
docker run -it -d --privileged=true  -v /package:/package  --name container_name -p 10022:22  192.168.3.153:5000/zrr/ice  /bin/bash

## 安装算法包(egg格式)：
easy_install  -i http://192.168.3.118:8080 violation_1625

## 镜像打包成tar文件：
docker save -o <保存路径> <镜像名称:标签>
docker save -o ./ubuntu18.tar ubuntu:18.04

## 镜像加载拷贝到服务器中：
docker load --input ./ubuntu18.tar

## 容器自动重启：
docker run --restart=always  （启动容器运行时加always参数）
docker update --restart=always <CONTAINER ID>（已经运行的容器update）

## Pycharm调试--ssh远程：
--> 进入容器
--> 修改root密码：passwd
--> 安装ssh服务：apt-get install openssh-server/apt-get install openssh-client
--> 修改ssh配置文件：vim /etc/ssh/sshd_config  :

	# PermitRootLogin prohibit-password # 默认打开禁止root用户使用密码登陆，需要将其注释
	RSAAuthentication yes #启用 RSA 认证
	PubkeyAuthentication yes #启用公钥私钥配对认证方式
	PermitRootLogin yes #允许root用户使用ssh登录

--> 重启sshd服务：/etc/init.d/ssh restart

## 查找匹配的文件： locate *.ttc

## 查看显存： nvidia-smi （加-l 1 表示每一秒钟刷新一次）

## 查看文件：tail -20 filename  (打印filename文件的后20行)

## Vim中跳到底部： G
## Vim中替换字符： :%s/1/2 （把所有的1替换成2）


## 容器更新备份成新镜像： docker commit 容器 新镜像名

## Python进程管理工具：supervisor (实现守护进程的功能)
Supervisord是用Python实现的一款非常实用的进程管理工具。supervisord会帮你把管理的应用程序转成daemon程序，而且可以方便的通过命令开启、关闭、重启等操作，而且它管理的进程一旦崩溃会自动重启，这样就可以保证程序执行中断后的情况下有自我修复的功能。

--> 安装supervisor: 可以下载安装包安装，也可以直接pip安装
--> 两个类型的命令：supervisord和supercisorctl（安装完成后在/user/bin下）
    配置supervisord: 
    执行：echo_supervisord_conf > /etc/supervisord.conf 
        （默认配置，如果权限报错，可以在其他文件生成再拷贝到/etc/supervisord.conf文件中）
    添加需要守护的进程program：在supervisord.conf文件的最后加上以下代码：
			[program:ice-0]   
			command=icegridnode --Ice.Config=config.grid
			directory=/package/second/new_image
			user=root
			autorestart=true
			redirect_stderr=true
			stdout_logfile=/package/second/new_image/log/ice_0.log
			loglevel=info
     其中：ice-0是进程名
          directory是进程项目地址
          command是进程项目启动命令  
          autorestart默认自动重启
          stdout_logfile日志输出
## Docker配置远程仓库地址：vim /etc/docker/daemon.json 
	将以下代码中的ip改成需要连接的远程仓库地址：
	{"insecure-registries":["192.168.3.153:5000"]}
    重启docker -- systemctl restart docker

## 镜像更新/上传/拉取（已配置远程仓库，否则需要docker login登录）：
	更新命令： docker commit <容器名或id> <镜像名或id:标签>
	提交命令：docker push <镜像名或id:标签>
	拉取docker命令： docker pull <镜像名或id:标签>
