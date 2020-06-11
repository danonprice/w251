import paho.mqtt.client as mqtt

output_dir = "./images"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("tx2/face")

# 9 tx2/face received!
# ./images/face-09.png

# Start counter
img_number = 0

def on_message(client, userdata, msg):
    global img_number
    print(str(img_number),msg.topic+" received!")
    
    if(img_number <10):
        img_name = output_dir + "/face-0" + str(img_number) + ".png"
    else:
        img_name = output_dir + "/face-" + str(img_number) + ".png"
    print(img_name)
    img_number = img_number + 1
    
    # Write image in Object Storage
    imgFile = open(img_name, 'wb')
    imgFile.write(msg.payload)
    imgFile.close()

client = mqtt.Client("ImageProcessor")
client.on_connect = on_connect
client.on_message = on_message

client.connect("172.19.0.2", 1883, 600)
client.loop_forever()
