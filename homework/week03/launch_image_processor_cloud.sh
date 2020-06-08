#!/bin/bash

# Create a bridge:
docker network create --driver bridge face_detect_net

# run mqtt broker
docker run --name mqtt_broker_0 --network face_detect_net -p 1883:1883 -ti mqtt_broker

# run image processor
docker run --name image_processor_0 --network face_detect_net -p 1883:1883 -ti image_processor