#!/bin/bash
# comment out any code you don`t need (tvm or mxnet)

set -e
set -u
set -o pipefail

# The so files mxnet needs 
chmod +x /install/files/mxnet/lib*
mv /install/files/mxnet/lib* /usr/local/cuda/lib64
cd /usr/local/cuda/lib64
ln -s libcublas.so.10.0.130 libcublas.so.10.0
ln -s libcufft.so.10.0.145 libcufft.so.10.0
ln -s libcurand.so.10.0.130 libcurand.so.10.0
ln -s libcusolver.so.10.0.130 libcusolver.so.10.0
ln -s libnvToolsExt.so.1.0.0 libnvToolsExt.so.1
rm -rf /install/files/mxnet/

# The so files tvm needs 
cd /install/files/tvm_so/
chmod +x lib*
mv libnvrtc.so.10.0.130 /usr/local/cuda/lib64/
mv libLLVM-8.so.1 /usr/lib/x86_64-linux-gnu/
mv libbsd.so.0.8.2 /lib/x86_64-linux-gnu/
mv libedit.so.2.0.53 /usr/lib/x86_64-linux-gnu/
cd /usr/local/cuda/lib64
ln -s libnvrtc.so.10.0.130 libnvrtc.so.10.0
cd /lib/x86_64-linux-gnu
ln -s libbsd.so.0.8.2 libbsd.so.0
cd /usr/lib/x86_64-linux-gnu
ln -s libedit.so.2.0.53 libedit.so.2
cd /install/files/tvm/python
python setup.py install
cd /install/files/tvm/topi/python/
python setup.py install
rm -rf /install/files/tvm /install/files/tvm_so
