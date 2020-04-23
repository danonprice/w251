import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as mqtt

MQTT_TOPIC = "tx2/face"
MQTT_HOST = "172.19.0.2"
MQTT_PORT = 1883
QOS = 2

def on_connect(client, userdate, flags, rc):
    if rc == 0:
        print("face detector connected to local broker with rc: " + str(rc))
        client.subscribe(MQTT_TOPIC)
    else:
        print("face detector not connected to broker")
        client.reconnect()

def on_message(client,userdata, msg):
  try:
    print("message received! - ",msg.topic)
    msg = msg.payload
    remote_mqttclient.publish(msg.topic, payload=msg.payload, qos=QOS, retain=False)
  except:
    print("unexpected error:", sys.exc_info()[0])

mqttclient = mqtt.Client("FaceDetector")
mqttclient.on_connect = on_connect
mqttclient.on_message = on_message
mqttclient.connect(MQTT_HOST,MQTT_PORT,600) # socket.timeout: timed out
mqttclient.loop_forever()

# mqttclient.publish(MQTT_TOPIC, payload=bytearray(cv.imencode('.png', crop_faces)[1]), qos=QOS, retain=False)
#time.sleep(5)
