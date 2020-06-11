#!/bin/bash

# Create a bridge:
docker network create --driver bridge face_detect_net

# run mqtt broker
docker run --name mqtt_broker_0 --network face_detect_net -p 1883:1883 -ti mqtt_broker

# run image processor
docker run --name image_processor_0 --network face_detect_net -p 1883:1883 -ti image_processor

s3fs w251-face-app /tmp/face -o passwd_file=$HOME/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.us-east.objectstorage.softlayer.net