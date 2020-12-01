## 第一步： 宿主机中安装docker（必须要19.0以上版本） -- docker -v查看版本
### 1. 卸载旧版本： 
    apt-get autoremove docker docker-ce docker-engine docker.io containerd runc
    apt-get autoremove docker* 

### 2. 安装新版本：
    apt-get update  （更新本地软件包索引）
    apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common （配置存储库）
    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -  （添加官方GPG密钥）
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"  （设置存储库类型，稳定版等）
    apt-get update
    apt-cache madison docker-ce  （查看支持的版本）
    apt-get install docker-ce docker-ce-cli containerd.io (最新稳定版，也可指定版本)
## 第二步： 从官方拉取相应版本的nvidia-docker -- 
 官方地址： [`10.0-base-ubuntu16.04` (*10.0/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu16.04/10.0/base/Dockerfile)

    nvidia-smi查看显卡驱动匹配的cuda版本，比如cuda版本 10.0,ubuntu版本 16.04，命令如下：
    docker pull nvidia/cuda:10.0-base-ubuntu16.04
    如果不确定cuda版本，尽量拉取低版本，如9.0版本等，版本向下兼容的
## 第三步： 安装nvidia-docker插件（即nvidia-container-toolkit插件）-- 
**ducker run --gpus all nvidia/cuda:9.0-base nvidia-smi 容器中能看到显卡即装成功**

    安装公钥
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    获取list
    curl -s -L https://nvidia.github.io/nvidia-docker/ubuntu16.04/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    更新
    sudo apt update
    安装nvidia-container-toolkit
    sudo apt install nvidia-container-toolkit
    重启
    sudo systemctl restart docker
## 第四步： 创建更新容器来制作新镜像（或者创建环境镜像的dockerfile来制作新的镜像）
**用第二步拉取下来的官方基础镜像创建一个容器，在容器中安装下面所有步骤的依赖环境**
docker run -itd --gpus all --name new_image_container nvidia/cuda:10.0-base-ubuntu16.04 bash

## 第五步： 安装python和相关扩展/三方（注意相关三方库的版本）：
     docker exec -it new_image_container bash
     apt-get update --fix-missing
     cd /var/lib/apt/lists/
     apt-get install -y python3.5 python3.5-dev
     apt-get install -y wget vim 
     wget  https://bootstrap.pypa.io/get-pip.py
     rm -rf /usr/bin/python /usr/bin/python3.5 && ln -s /usr/bin/python3.5 /usr/bin/python3 && ln -s /usr/bin/python3.5 /usr/bin/python

     python get-pip.py 
     apt-get update
     apt-get install -y libglib2.0-0
     apt-get install -y python3.5-qt4
     rm -rf *

     pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/  numpy==1.17.0 supervisor==4.0.4
     pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ torch==0.4.1 torchvision==0.2.1 
     pip install -i https://mirrors.aliyun.com/pypi/simple/ Pillow==6.1.0

## 第六步： 安装/编译TVM以及相关依赖：
### 1. 下载TVM源码：
    git clone --recursive https://github.com/apache/incubator-tvm tvm

    apt-get install cmake gcc g++
### 2. 安装llvm:
    $ wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key| apt-key add -
    $ sudo apt-add-repository "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-8.0 main"
    $ sudo apt-get update
    $ sudo apt-get install -y clang-8.0
### 3. 安装其他依赖：
    apt-get install libedit-dev
    apt-get install libxml2-dev
    apt-get install build-essential
    apt-get install libtinfo-dev
    apt-get install zliblg-dev
    
### 4. 开始编译：
    cd tvm
    mkdir build
    cp cmake/config.cmake build
    vim build/config.cmake -- 
       修改：set(USE_CUDA OFF)  --> set(USE_CUDA ON)
       set(USE_LLVM /path/to/llvm/bin/llvm-config)
    cd build
    cmake ..
    make -j4
    安装TVM库：
    方法一：环境变量
    vim ~/.bashrc --
       export TVM_HOME=/path/to/tvm
       export PYTHONPATH=$TVM_HOME/python:$TVM_HOME/topi/python:${PYTHONPATH}
    source ~/.bashrc 
    方法二：利用setup.py安装
		cd python; python setup.py install --user; cd ..
		cd topi/python; python setup.py install --user; cd ../..
    pip install --user numpy decorator attrs
    pip install --user tornado psutil xgboost
    pip install --user mypy orderedset antlr4-python3-runtime
### 5. 测试是否安装编译成功：
    进入python3.5的shell环境，能import tvm则编译成功

## 第七步： commit提交镜像：
**注意：在退出容器前，为了保证容器尽可能的小，删除掉无用的文件，比如/var/lib/apt/lists/下面的所有文件和tvm的相关文件**

    删除无用文件，退出容器，执行下面代码打包/提交做好的新镜像：
	docker commit 镜像名 仓库地址：标签
	docker push 仓库地址：标签



https://github.com/pypa/pip/issues/5599


easy_install -i http://192.168.3.118:8080 police_classification vehicle_re_recognition license_plate_color_detection violation_1019 violation_1208 violation_1211 violation_1345 violation_1625 day_night_detection day_night_classification pedestrian_detection traffic_light_detection vehicle_type_detection license_plate_detection license_plate_recognition 
vehicle-detection-m2det


easy_install -i http://192.168.3.118:8080 vehicle-flow-statistics vehicle-re-recognition staff-classification smoke-phone-classification retinaface-recogition-tvm-1080ti person-vehicle-confirm pedestrian-vehicle-detection mask-classification license-plate-recognition license-plate-detection image-unnormal-roi-cut glove-hat-detection fire-detection-centernet extinguisher-mat-classification electrostastic-device-detection abandoned-roi-detection 