#!/bin/bash

set -e
set -u
set -o pipefail

# install libraries for python package on ubuntu
pip install -i https://mirrors.aliyun.com/pypi/simple/ psutil==5.6.3 scikit-image==0.15.0 scikit-learn==0.21.3 numpy==1.18.2 supervisor==4.1.0 opencv-python==4.1.0.25 Pillow==6.1.0 requests

# mxnet (if you don`t need this, commenout this code)
pip install -i https://mirrors.aliyun.com/pypi/simple/ mxnet-cu100

# torch (if you don`t need this, commenout this code)
pip install -i https://mirrors.aliyun.com/pypi/simple/ torch==0.4.1 torchvision==0.2.1

# other library (if you don`t need this, commenout this code)
pip install -i https://mirrors.aliyun.com/pypi/simple/ cffi==1.14.0 addict==2.2.1 Cython==0.29.13 progress==1.5 termcolor==1.1.0 decorator==4.4.2
pip install -i https://mirrors.aliyun.com/pypi/simple/ kafka-python==1.4.6 py3nvml==0.2.6 redis==3.4.1 tornado==6.0.4 APScheduler==3.6.1
