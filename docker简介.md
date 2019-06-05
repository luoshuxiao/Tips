# Docker简单操作：
**Docker是一个为开发者和系统管理员在容器中开发、部署和运行的平台，灵活、轻量级、可互换、部署简单、扩展性极强的容器**
### a. 镜像image和容器container
	镜像是一个包含所有需要运行的文件组成的包，比如代码、可运行文件、库、
        环境变量和配置文件等；
	容器是镜像运行的一个实列，是运行镜像后产生的；
	容器和虚拟机区别：
	容器和进程一样直接在主机操作系统上运行，不占用更多的资源；
	虚拟机直接模拟一个虚拟操作系统，程序实在模拟操作系统里面运行，占用更多资源；

	Docker CE -- 代表社区版本
	Docker EE -- 代表企业版本

### b. 安装Docker
		第一步： 安装yum-utils -- 
		sudo yum install -y yum-utils 
		
		第二步： 设置稳定版本的repository仓库(最好不要装不稳定版本的docker)
		
		sudo yum-config-manager --add-repo https://docs.docker.com/engine/installation/linux/repo_files/ubuntu/docker.repo
		
		sudo apt-get update  # 更新 
		
		第三步： 安装并启动docker社区版
		
		sudo apt-get install docker-ce
		sudo systemctl start docker 或者 service start docker
		
		验证时候安装成功： sudo docker run hello-world (出现一堆代码，包含了hello from docker，说明安装并启动成功)
		
		卸载docker命令: sudo yum remove docker-ce 或者 sudo rm -rf varlib/docker
		查看docker版本： docker version
		查看docker信息： docker info
		列出docker下所有容器： docker image ls     
		  
		第四步： 在docker中运行自己的项目（整体搬迁运行影像）
		**需要Dockerfile进行配置，Dockerfile定义了容器内的环境**
		
		mkdir docker_test  (可以创建在home目录下)
		cd docker_test
		vim Dockerfile # 将下面代码写入Dockerfile(根据项目具体情况设置具体参数)
				
				# Use an official Python runtime as a parent image
				FROM python:2.7-slim
				# Set the working directory to /app
				WORKDIR /app
				# Copy the current directory contents into the container at /app
				ADD . /app
				# Install any needed packages specified in requirements.txt
				RUN pip install -i https://pypi.douban.com/simple -r requirements.txt
				# Make port 80 available to the world outside this container（docker容器内部端口）
				EXPOSE 80
				# Define environment variable
				ENV NAME World
				# Run app.py when the container launches (一般是manage.py)
				CMD ["python", "app.py"]
		vim requirements.txt # 需要导入的pyhton包
		        Flask
		        Redis
		将项目的代码拷贝到docker_test文件夹下（这里的测试的项目代码是 app.py）
		
		第五步：创建docker镜像(最后有一个点符号)
		docker build -t first_docker .
		docker image ls (查看已有镜像或者docker images)
		
		第六步： 重启docker
		service docker restart 或者systemctl restart docker
		
		第七步： 运行容器
		docker run -p 4000:80 first_docker
		
		查看启动的docker容器： docker ps
		停止指定的docker容器： docker container stop 85ac7faf8ea3
                             docker stop  85ac7faf8ea3
        删除指定的容器： docker rm 85ac7faf8ea3
        进入容器： docker exec -it e1066fe2db35 /bin/bash 
                  docker exec 是docker镜像的连接命令，类似ssh一样
## c. 相关命令
        查看已有容器：docker ps (正在运行的)
                    docker ps -a (所有容器，包括停止的)
		镜像打包成tar文件：
		docker save -o <保存路径> <镜像名称:标签>
		docker save -o ./ubuntu18.tar ubuntu:18.04
		
		镜像加载拷贝到服务器中：
		docker load --input ./ubuntu18.tar
		
		容器自动重启：
		docker run --restart=always  （启动容器运行时加always参数）
		docker update --restart=always <CONTAINER ID>（已经运行的容器update）
## d. docker hub仓库 和daocloud镜像仓库
**docker hub是国外的平台，连接速度可能比较慢，所以国内一般在daocloud管理镜像**

	注册daocloud平台：
	
	在daocloud平台注册账号密码，然后创建自己的组织
	
	登录daocolud平台：
	docker login daocloud.io # 输出账号、密码
	
	给要上传云平台的镜像打标签(v1)：
	docker tag first_docker daocloud.io/my_team/first_docker:v1
	上传镜像：
	docker push daocloud.io/my_team/first_docker:v1
	
	从服务器拉取镜像并运行容器：
	docker run -p 4000:80 daocolud.io/my_team/seconds_docker:v1