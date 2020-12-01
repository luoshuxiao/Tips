## 模块：
### logging -- 日志模块
### struct -- 数据的打包/解包（二进制）
### textwrap -- 字符串文本样式处理模块
### configparser -- 读取配置文件（配置文件中将一些参数可配置化）
### traceback -- 捕获、打印全面的异常信息
### difflib -- 文件内容差异对比模块
### supervisor -- 进程管理模块（可以配合docker进行自动化部署）
### zero-ice -- python实现ice通信框架模块

## 启动docker容器(markdown直接复制到命令行执行，会报错no such file or directory,其他地方复制到命令行就可以，markdown的bug)：
docker run -it -d --privileged=true  -v /package:/package  --name test -p 10022:22  192.168.3.153:5000/lsx:2.0  /bin/bash
docker run -itd --privileged=true  -v /package:/package  --name tt  192.168.3.153:5000/lsx:2.0  /bin/bash

## 镜像打包成tar文件：
docker save -o <保存路径> <镜像名称:标签>
docker save -o ./ubuntu18.tar ubuntu:18.04

## 镜像重命名：
docker tag 镜像id 仓库：标签

## 镜像加载拷贝到服务器中：
docker load --input ./ubuntu18.tar

## 容器自动重启：
docker run --restart=always  （启动容器运行时加always参数）
docker update --restart=always <CONTAINER ID>（已经运行的容器update）

## docker容器和宿主机之前的文件拷贝
docker cp 宿主机文件路径 容器名：容器内路径
docker cp 容器名：容器内路径 宿主机文件路径

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

## 查看文件：
        tail -20 filename  (打印filename文件的后20行)
        tail -20f filname (滚定打印文件的最后20行，实时更新)
## Vim中跳到底部： G
## Vim中替换字符： :%s/1/2 （把所有的1替换成2）
## vim中光标跳转到指定行： 行数gg 
## vim删除当前行： dd

## 容器更新备份成新镜像： docker commit 容器 新镜像名

## Python进程管理工具：supervisor (实现守护进程的功能)
**supervisor有网页版可视化管理界面，ip是布置supervisor工具的服务器ip,端口是默认端口3999**
	Supervisord是用Python实现的一款非常实用的进程管理工具。supervisord会帮你把管理的应用程序转成
    daemon程序，而且可以方便的通过命令开启、关闭、重启等操作，而且它管理的进程一旦崩溃会自动重启，这
    样就可以保证程序执行中断后的情况下有自我修复的功能。

	--> 安装supervisor: 可以下载安装包安装，也可以直接pip安装
	--> 两个类型的命令：supervisord和supercisorctl（安装完成后在/user/bin下）
	
	    配置supervisord: 
	    执行：echo_supervisord_conf > /etc/supervisord.conf 
	        （默认配置，如果权限报错，可以在其他文件生成再拷贝到/etc/supervisord.conf文件中）
             supervisord.conf文件中，可以配置日志文件最大值，和日志保存的文件数量等等；

	    添加需要守护的进程program：在supervisord.conf文件的最后加上以下代码：
          （也可以单独写一个配置进程的文件，包含进supercisord.conf文件中）
				[program:ice-0]   
				command=icegridnode --Ice.Config=config.grid
				directory=/package/second/new_image
				user=root
				autorestart=true
				redirect_stderr=true
				stdout_logfile=/package/second/new_image/log/ice_0.log
				loglevel=info
	     其中：ice-0是进程名
	          directory是进程项目的地址
	          command是进程项目启动命令
	          autorestart默认自动重启
	          stdout_logfile日志输出
        启动命令： /usr/local/bin/supervisord -c /etc/supervisord.conf 

        可以登录网址查看/管理 supervisor 运行状态：
             http://服务器ip:端口   (账号密码端口在supervisord.conf文件中有配置)
## Docker配置远程仓库地址：vim /etc/docker/daemon.json 
	将以下代码中的ip改成需要连接的远程仓库地址：
	{"registry-mirrors": ["https://3c9ywpon.mirror.aliyuncs.com"]，"insecure-registries":["192.168.3.153:5000"]}
    "registry-mirrors"是配置镜像源（国外镜像源网速慢，可配置国内镜像源，阿里镜像源等）；
    如果有多个私有仓库要链接，将其他私有仓库地址添加到这个json文件"insecure-registries"的值的列表中就行；
    重启docker -- systemctl restart docker

## 镜像更新/上传/拉取（已配置远程仓库，否则需要docker login登录）：
	更新命令： docker commit <容器名或id> <镜像名或id:标签>
	提交命令：docker push <镜像名或id:标签>
	拉取docker命令： docker pull <镜像名或id:标签>

## linux命令：
    scp文件传送：
		本地到远程 -->  scp /package/second-2.2.tar hadoop@192.168.3.210:/package/
		远处到本地 -->  scp root@192.168.3.210:/opt/soft/nginx-0.5.38.tar.gz  /opt/soft/
        当需要传送文件夹时，在scp后添加 -r 参数，否则会报错：not a regular file；
    查看cpu信息： cat /proc/cpuinfo
    查看系统体系结构：uname -a
    查看系统内核：uname -r
    查看显卡驱动： nvidia-smi
    查看显卡驱动（每秒刷新）：nvidia-smi -l 1
    查看系统加载的某个模块以及相关依赖项： lsmod | grep -i nvidia (显卡驱动)
    查看使用的编码字符集： locale
## linux显卡卸载/安装：
	卸载：方式一：
	        sudo ./NVIDIA-Linux-x86_64-418.56.run --uninstall
	     方式二：
	        sudo apt-get --purge remove nvidia* 
	        或者：sudo apt-get remove --purge '^nvidia-.*'
	     （网上还有其他很多方式）
	安装：第一种(.run文件或者.deb文件安装)：
	         第一步 -- 官网下载需要的nvidia版本（.run文件）
		     第二步 -- service lightdm stop （关闭 X server）
		     第三步 -- sudo init 3 或者sudo telinit 3 (停止可视化界面)
		     第四步 -- sudo sh NVIDIA*.run –no-opengl-files
		              或者 dpkg -i nvidia-diag-driver-local-repo-ubuntu1604_375.66-1_amd64.deb
         第二种（ppa自动安装）：
			sudo add-apt-repository ppa:graphics-drivers/ppa  (将图形驱动程序PPA存储库添加到系统中)
			sudo apt update  （更新系统）
			ubuntu-drivers devices  （识别显卡模型和推荐的驱动程序）
			sudo apt-get install nvidia-390  （安装指定版本的驱动程序）

        reboot  (安装成功后重启电脑)
        nvidia-smi (查看驱动安装是否成功)

    问题（系统可能会自动更新驱动）：如果安装成功后，第二天或者隔一段时间nvidia-smi就没有输出，报以下错误：
                Failed to initialize NVML: driver/library version mismatch，
         可能是因为nvidia自动更新了版本，但是nvidia内核版本没更新，用命令：
               vim /etc/apt/apt.conf.d/50unattended-upgrades ，
         将Unattended-Upgrade::Allowed-Origins里面的所有选项注释掉，关闭自动更新功能，
         然后重新装需要的nvidia版本，装成功后重启电脑；

         或者输入命令 ： echo "nvidia-390 hold" | sudo dpkg --set-selections
## linux只能访问内网，不能访问外网（可以设置成这种模式）：
**现象：ping www.baidu.com ，ping不通，但是ping内网能ping通**

    可能原因：网关设置有问题，防火墙, DNS，网卡等等原因；
    解决措施（可能能解决）：
       1. 设置网卡，ip: vim /etc/sysconfig/network-scripts/ifcfg-eth0
	       	DEVICE=eth0 #描述网卡对应的设备别名，例如ifcfg-eth0的文件中它为eth0   
			BOOTPROTO=static #设置网卡获得ip地址的方式，可能的选项为static，dhcp或bootp，分别对应静态指
                              定的ip地址，通过dhcp协议获得的ip地址，通过bootp协议获得的ip地址   
			BROADCAST=192.168.0.255 #对应的子网广播地址   
			HWADDR=00:07:E9:05:E8:B4 #对应的网卡物理地址   
			IPADDR=192.168.0.2 #如果设置网卡获得 ip地址的方式为静态指定，此字段就指定了网卡对应的ip地址   
			IPV6INIT=no   
			IPV6_AUTOCONF=no   
			NETMASK=255.255.255.0 #网卡对应的网络掩码   
			NETWORK=192.168.0.0 #网卡对应的网络地址   
			ONBOOT=yes #系统启动时是否设置此网络接口，设置为yes时，系统启动时激活此设备
       设置好后，重启网卡：service network restart 
       ping www.baidu.com 能ping通，说明成功解决，不能ping通，进行第2步，设置网关路由

       2. 设置网关路由：
	       使用命令查看路由表信息：netstat -r 
	       default 项是localost或者正确的网关ip，那么应该是正确的；
	       如果不正确，使用命令：route add default gw 网关ip 添加正确的网关ip
                删除错误的路由： route add default gw 网关ip
       设置好后，ping www.baidu.com 能ping通，说明成功解决，
       如果不能ping通，报错：ping www.baidu.com unknow host.... 进行第3步，设置DNS
       注意： 设置路由的操作在重启电脑后会失效，想要重启不失效，可以用命令-- vim /etc/rc.local ，
              在代码： exit 0 的前一行添加相应的route命令

       3. 设置DNS域名解析:
       vim /etc/resplv.conf 

       添加以下内容：
           nameserver 202.106.0.20
           nameserver 202.106.196.115
       重启网卡：service network restart
       ping www.baidu.com 能ping通，说明成功解决。

## 国内镜像源：
	  阿里云 http://mirrors.aliyun.com/pypi/simple/ 
	  中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/ 
	  豆瓣(douban) http://pypi.douban.com/simple/ 
	  清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/ 
	  中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/

## 编码问题：

PYTHONIOENCODING=utf-8 nohup python server.py &