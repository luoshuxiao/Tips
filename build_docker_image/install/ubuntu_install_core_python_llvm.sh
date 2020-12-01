#!/bin/bash

set -e
set -u
set -o pipefail

apt-get update && apt-get install -y --no-install-recommends \
        make libgtest-dev cmake wget vim libtinfo-dev libz-dev\
        libcurl4-openssl-dev libopenblas-dev g++ apt-transport-https

cd /usr/src/gtest && cmake CMakeLists.txt && make && cp *.a /usr/lib

apt-get install -y software-properties-common

add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y python-pip python-dev python3.5 python3.5-dev
apt-get install libsm6 libxrender1 libxext6 tzdata

rm -f /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/python3.5 /usr/bin/python3 && ln -s /usr/bin/python3.5 /usr/bin/python

echo deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-8 main\
     >> /etc/apt/sources.list.d/llvm.list
echo deb-src http://apt.llvm.org/xenial/ llvm-toolchain-xenial-8 main\
     >> /etc/apt/sources.list.d/llvm.list

wget -q -O - http://apt.llvm.org/llvm-snapshot.gpg.key| apt-key add -
apt-get update && apt-get install -y llvm-8 clang-8
cd /
wget https://bootstrap.pypa.io/get-pip.py
# python get-pip.py
# rm -rf get-pip.py

# pip install -i https://mirrors.aliyun.com/pypi/simple/ decorator xgboost antlr4-python3-runtime progress==1.5 psutil==5.6.3 py3nvml redis scikit-image==0.15.0 scikit-learn==0.21.3 supervisor
# pip install -i https://mirrors.aliyun.com/pypi/simple/ addict==2.2.1 APScheduler==3.6.1 cffi Cython==0.29.13 kafka-python==1.4.6 opencv-python==4.1.0.25 Pillow==6.1.0 termcolor
# pip install -i https://mirrors.aliyun.com/pypi/simple/ torch==0.4.1  
# pip install -i https://mirrors.aliyun.com/pypi/simple/ torchvision==0.2.1
