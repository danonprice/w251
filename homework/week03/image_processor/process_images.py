import paho.mqtt.client as mqtt

MQTT_HOST = "mqtt_broker_remote"
MQTT_PORT = 1883
MQTT_TOPIC = "tx2/face"
QOS = 2

# volume attached to s3 mount
output_dir = "/home/image_processor/images"

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)
    print("Connected to",MQTT_HOST,"with result code",str(rc))
    print("Subscribed to topic",MQTT_TOPIC)
    
# image counter
img_number = 0

def on_message(client, userdata, msg):
    global img_number

    if(img_number < 10):
        img_name = output_dir + "/face-0" + str(img_number) + ".png"
    else:
        img_name = output_dir + "/face-" + str(img_number) + ".png"

    # Write image in Object Storage
    imgFile = open(img_name, 'wb')
    imgFile.write(msg.payload)
    imgFile.close()
    
    print("Image",str(img_number),msg.topic+" received and saved to",img_name)

    img_number = img_number + 1    

client = mqtt.Client("ImageProcessor")
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 600)
client.loop_forever()
