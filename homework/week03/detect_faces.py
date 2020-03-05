import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as mqtt

def on_connect(mqtt_client,userdate,flags,rc):
    if rc == 0:
        print("Successfully Connected")
    else:
        print("Not Connected")
        mqtt_client.reconnect()

def on_publish(mqtt_client,userdate,mid):
    print("Face Published")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.connect("iot.eclipse.org",1883,60) # socket.timeout: timed out
#mqtt_client.connect("127.0.0.1",1883,60) #ConnectionRefusedError: Connection refused
#mqtt_client.connect("localhost",1883,60) # OSError: Cannot assign requested address
#mqtt_client.connect("mosquitto",1883,60) # socket.gaierror: No address associated with hostname
#mqtt_client.connect("52.116.3.158",1883,60) # socket.timeout: timed out

#time.sleep(1)

cap = cv.VideoCapture(1)
                                
cascade = cv.CascadeClassifier("/home/face_detection/haarcascade_frontalface_default.xml")

mqtt_client.loop_start()

while(True):
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.3, 5)
    cv.imshow('frame',gray)

    for (x,y,w,h) in faces:
        crop_faces = gray[y:y+h,x:x+w]
        cv.imshow("crop", crop_faces)
        #mqtt_client.publish("tx2/face", bytearray(cv.imencode('.png', crop_faces)[1]), qos=1)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

mqtt_client.loop_stop()
mqtt_client.disconnect()
cap.release()
cv.destroyAllWindows()
