#!/bin/bash

# Create a bridge:
docker network create --driver bridge face_detect_net
echo "created network bridge"

# run mqtt broker
#docker run --name mqtt_broker_0 --network face_detect_net -p 1883:1883 -ti mqtt_broker
docker run --network face_detect_net -p 1883:1883 -ti mqtt_broker
echo "running broker"

# run mqtt message forwarder
#docker run --name mqtt_forwarder_0 --network face_detect_net -ti mqtt_forwarder
docker run --network face_detect_net -ti mqtt_forwarder
echo "running forwarder"

# run face detector
xhost +
docker run -e DISPLAY=$DISPLAY --rm --privileged -v /tmp:/tmp -ti face_detector
