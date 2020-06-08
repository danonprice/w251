import paho.mqtt.client as mqtt
import cv2 as cv

#output_dir = "/home/image_processor/images"
output_dir = "./images"
# https://w251-face-app.s3.us-east.cloud-object-storage.appdomain.cloud

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("tx2/face")

# Start counter
img_number = 0

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global img_number
    print(str(img_number),msg.topic+" received!")
    # print("message = ",msg.payload)
    # De-encode message
    #f = np.frombuffer(msg.payload, dtype='uint8')
    #img = cv.imdecode(msg.payload, flags=1)
    #img = cv.imdecode(msg.payload)
    #print(img.shape)
    
    # Save messages, keeping numeration of stream
    if(img_number <10):
        img_name = output_dir + "/face-0" + str(img_number) + ".png"
        print(img_name)
    else:
        img_name = output_dir + "/face-" + str(img_number) + ".png"
        print(img_name)
    img_number = img_number + 1
    
    # Write image in Object Storage
    #cv.imwrite(img_name, img)
    imgFile = open(img_name, 'wb')
    imgFile.write(msg.payload)
    imgFile.close()

client = mqtt.Client("ImageProcessor")
client.on_connect = on_connect
client.on_message = on_message

client.connect("172.19.0.2", 1883, 600)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
