#!/bin/bash

set -e
set -u
set -o pipefail

apt-get update && apt-get install -y --no-install-recommends libopenblas-dev\
        libgtest-dev wget vim libtinfo-dev libz-dev unzip

apt-get install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y python-pip python-dev python3.5 python3.5-dev python3-pip

rm -f /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/python3.5 /usr/bin/python3 && ln -s /usr/bin/python3.5 /usr/bin/python
cd /
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
rm -rf get-pip.py
apt-get update
apt-get install -y libsm6 libxrender1 libxext6 tzdata libglib2.0-dev
# pip install -i https://mirrors.aliyun.com/pypi/simple/ decorator progress==1.5 psutil==5.6.3 py3nvml redis scikit-image==0.15.0 scikit-learn==0.21.3 supervisor
# pip install -i https://mirrors.aliyun.com/pypi/simple/ addict==2.2.1 APScheduler==3.6.1 cffi Cython==0.29.13 kafka-python==1.4.6 opencv-python==4.1.0.25 Pillow==6.1.0 termcolor
# pip install -i https://mirrors.aliyun.com/pypi/simple/ torch==0.4.1  
# pip install -i https://mirrors.aliyun.com/pypi/simple/ torchvision==0.2.1 tornado requests
