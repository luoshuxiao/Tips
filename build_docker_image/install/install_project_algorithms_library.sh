#!/bin/bash

set -e
set -u
set -o pipefail

# traffic_server project
easy_install -i http://192.168.3.118:8080 police_classification vehicle_re_recognition license_plate_color_detection violation_1019 violation_1208 violation_1211 violation_1345 violation_1625 day_night_detection day_night_classification pedestrian_detection traffic_light_detection vehicle_type_detection license_plate_detection license_plate_recognition vehicle-detection-m2det

# gas_server project
easy_install -i http://192.168.3.118:8080 vehicle-flow-statistics vehicle-re-recognition staff-classification smoke-phone-classification retinaface-recogition-tvm-1080ti person-vehicle-confirm pedestrian-vehicle-detection mask-classification license-plate-recognition license-plate-detection image-unnormal-roi-cut glove-hat-detection fire-detection-centernet extinguisher-mat-classification electrostastic-device-detection abandoned-roi-detection 

# face_welcome project
easy_install -i http://192.168.3.118:8080 retinaface-recogition-tvm-1080ti mobile_face

# weixin_server project
easy_install -i http://192.168.3.118:8080 retinaface-recogition-tvm-1080ti fire-detection-centernet license_plate_detection license_plate_recognition vehicle-detection-m2det

# virus_server project 
easy_install -i http://192.168.3.118:8080 staff-classification person-vehicle-confirm pedestrian-vehicle-detection mask-classification license_plate_detection license_plate_recognition