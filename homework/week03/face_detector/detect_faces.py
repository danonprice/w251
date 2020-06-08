import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as mqtt

MQTT_TOPIC = "tx2/face"
MQTT_HOST = "172.18.0.2"
MQTT_PORT = 1883
QOS = 2

def on_connect(client, userdate, flags, rc):
    if rc == 0:
        print("face detector connected to local broker with rc: " + str(rc))
    else:
        print("face detector not connected to broker")
        client.reconnect()

def on_publish(mqttclient,userdate,msgid):
    print("face published to local broker - ",msgid)

mqttclient = mqtt.Client("FaceDetector")
mqttclient.on_connect = on_connect
mqttclient.on_publish = on_publish
mqttclient.connect(MQTT_HOST,MQTT_PORT,600) # socket.timeout: timed out
#mqttclient.connect("iot.eclipse.org",1883,60) # socket.timeout: timed out
#mqttclient.connect("127.0.0.1",1883,60) #ConnectionRefusedError: Connection refused
#mqttclient.connect("localhost",1883,60) # OSError: Cannot assign requested address
#mqttclient.connect("mosquitto",1883,60) # socket.gaierror: No address associated with hostname
#mqttclient.connect("52.116.3.158",1883,60) # socket.timeout: timed out
mqttclient.loop_start()
#time.sleep(5)

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
        #mqttclient.publish(MQTT_TOPIC, payload=bytearray(cv.imencode('.png', crop_faces)[1]), qos=QOS, retain=False)
        byteArr = bytearray(crop_faces)
        mqttclient.publish(MQTT_TOPIC, payload=byteArr, qos=QOS, retain=False)
        #time.sleep(5)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

mqttclient.loop_stop()
mqttclient.disconnect()
cap.release()
cv.destroyAllWindows()
