# docker GPU env
# tag: v0.60
FROM nvidia/cuda:10.0-base-ubuntu16.04

# Base scripts
COPY install/ubuntu_install_python.sh /install/ubuntu_install_python.sh
RUN bash /install/ubuntu_install_python.sh

# install the necessary packages about python
COPY install/ubuntu_install_python_package.sh /install/ubuntu_install_python_package.sh
RUN bash /install/ubuntu_install_python_package.sh

# install the environment of tvm or mxnet and the necessary so libraries
ADD install/files/ /install/files/
COPY install/install_tvm_mxnet_so.sh /install/install_tvm_mxnet_so.sh
RUN bash /install/install_tvm_mxnet_so.sh

# install algorithms libraries of project
COPY install/install_project_algorithms_library.sh /install/install_project_algorithms_library.sh
RUN bash /install/install_project_algorithms_library.sh

ENV PYTHONIOENCODING=utf-8
ENV PATH=/usr/local/nvidia/bin:${PATH}
ENV PATH=/usr/local/cuda/bin:${PATH}
ENV CPLUS_INCLUDE_PATH=/usr/local/cuda/include:${CPLUS_INCLUDE_PATH}
ENV C_INCLUDE_PATH=/usr/local/cuda/include:${C_INCLUDE_PATH}
ENV LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda/compact:${LIBRARY_PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda/compact:${LD_LIBRARY_PATH}
