#! /bin/bash

# Create a bridge:
docker network create --driver bridge face_detect_net
echo "Created network bridge"

cd mqtt_broker
sudo docker build -t mqtt_broker -f Dockerfile.mqtt_broker .

cd ../mqtt_forwarder
sudo docker build -t mqtt_forwarder -f Dockerfile.mqtt_forwarder .

cd ../face_detector
sudo docker build -t face_detector -f Dockerfile.face_detector .
