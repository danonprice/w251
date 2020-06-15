#! /bin/bash

# Create a bridge:
docker network create --driver bridge face_detect_net

# run mqtt broker
docker run -d --name mqtt_broker_remote --network face_detect_net -p 1883:1883 mqtt_broker

# run image processor
docker run --rm -ti --privileged --name image_processor_0 -v /mnt/face:/home/image_processor/images --network face_detect_net -w /home/image_processor image_processor