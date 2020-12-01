easy_install -i http://192.168.3.118:8080 abandoned-roi-detection car-retrograde-classify electrostatic_discharge_detection electrostatic-shoes-classify extinguisher-mat-classification fire-detection-centernet glove-hat-detection image-unnormal-roi-cut license-plate-detection license-plate-recognition oil-gas-interface-detection oil-interface-detection oil_cup_size_classify oil-tube-abnormal-classify pedestrian-vehicle-detection person-pose-classify person-vehicle-confirm play_phone retinaface-recogition-tvm-1080ti sit-rail-classify smoke-detection-centernet smoke-phone-classification staff-classification
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ opencv-contrib-python==3.4.2.16 pyyaml
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
echo 'Asia/Shanghai' >/etc/timezone
rm -f /package/install.sh
