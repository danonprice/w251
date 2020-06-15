import paho.mqtt.client as mqtt


REMOTE_MQTT_HOST = "52.116.3.98" #"192.168.1.24"
LOCAL_MQTT_HOST = "mqtt_broker_tx2"
MQTT_PORT = 1883
MQTT_TOPIC = "tx2/face"
QOS = 2

def on_connect_local(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)
    print("Connected to",LOCAL_MQTT_HOST,"with result code",str(rc))
    print("Subscribed to topic",MQTT_TOPIC)

def on_connect_remote(client, userdata, flags, rc):
    print("Connected to",REMOTE_MQTT_HOST,"with result code",str(rc))

def on_message(client,userdata, msg):
    global remote_mqttclient
    try:
        print("Message received on topic",msg.topic)
        remote_mqttclient.publish(msg.topic, payload=msg.payload, qos=QOS, retain=False)
    except:
        print("Message error:", sys.exc_info()[0])

def on_publish(client, userdata, msgid):
    print("Message",msgid,"published to remote server",REMOTE_MQTT_HOST)

def on_disconnect_local(client, userdata, rc):
    client.loop_stop()


local_mqttclient = mqtt.Client("TX2-Forward")
local_mqttclient.on_connect = on_connect_local
local_mqttclient.on_message = on_message
local_mqttclient.on_disconnect = on_disconnect_local

remote_mqttclient = mqtt.Client("Remote-Forward")
remote_mqttclient.on_connect = on_connect_remote
remote_mqttclient.on_publish = on_publish

local_mqttclient.connect(LOCAL_MQTT_HOST, MQTT_PORT, 600)
local_mqttclient.loop_start()

remote_mqttclient.connect(REMOTE_MQTT_HOST, MQTT_PORT, 600)
remote_mqttclient.loop_forever()
