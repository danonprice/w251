#!/bin/bash

sudo

# create network bridge
sudo docker network create --driver bridge face_detect_net
echo "Created network bridge"

# run mqtt broker
sudo docker run -d --name mqtt_broker_tx2 --network face_detect_net -p 1883:1883 mqtt_broker
echo "Running MQTT broker"

# run mqtt message forwarder
sudo docker run -d --rm --name mqtt_forwarder_0 --network face_detect_net -w /home/forwarder mqtt_forwarder
echo "Running MQTT forwarder"

# run face detector
xhost +
sudo docker run -e DISPLAY=$DISPLAY --rm --privileged -v /tmp:/tmp -ti face_detector
