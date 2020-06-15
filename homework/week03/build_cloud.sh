#! /bin/bash

docker network create --driver bridge face_detect_net &
echo "Created network bridge"

cd mqtt_broker
docker build -t mqtt_broker -f Dockerfile.mqtt_broker .

cd ../image_processor
docker build -t image_processor -f Dockerfile.image_processor .

echo "Built cloud MQTT broker and Image Processor"