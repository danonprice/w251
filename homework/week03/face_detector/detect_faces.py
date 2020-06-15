import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as mqtt

MQTT_HOST = "mqtt_broker_tx2"
MQTT_PORT = 1883
MQTT_TOPIC = "tx2/face"
QOS = 2

def on_connect(client, userdate, flags, rc):
    print("Connected to",MQTT_HOST,"with result code",str(rc))

def on_publish(client, userdate, msgid):
    print("Message",msgid,"published to local server",MQTT_HOST)

mqttclient = mqtt.Client("FaceDetector")
mqttclient.on_connect = on_connect
mqttclient.on_publish = on_publish
mqttclient.connect(MQTT_HOST,MQTT_PORT,600)
mqttclient.loop_start()

cap = cv.VideoCapture(1)
cascade = cv.CascadeClassifier("/home/face_detection/haarcascade_frontalface_default.xml")

while(True):
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.3, 5)
    cv.imshow('frame',gray)

    for (x,y,w,h) in faces:
        crop_faces = gray[y:y+h,x:x+w]
        cv.imshow("crop", crop_faces)
        cv.imwrite("face.png",crop_faces)

        f=open("face.png", "rb")
        fileContent = f.read()
        byteArr = bytearray(fileContent)
        mqttclient.publish(MQTT_TOPIC, payload=byteArr, qos=QOS, retain=False)

        time.sleep(5)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

mqttclient.loop_stop()
mqttclient.disconnect()
cap.release()
cv.destroyAllWindows()
