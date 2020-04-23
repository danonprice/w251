import paho.mqtt.client as mqtt

MQTT_TOPIC = "tx2/face/#"
QOS = 2

LOCAL_MQTT_HOST = "172.18.0.2"
MQTT_PORT = 1883

REMOTE_MQTT_HOST = "192.168.1.24" #"172.19.0.2"

def on_connect_local(client, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_subscribe(client, userdata, msgid, qos):
    print("subscribed to topic ",MQTT_TOPIC)

def on_connect_remote(client, userdata, flags, rc):
    print("connected to remote broker with rc: " + str(rc))
    #client.subscribe(MQTT_TOPIC)

def on_message(client,userdata, msg):
  global remote_mqttclient
  try:
    print("message received - ",msg.topic)
    remote_mqttclient.publish(msg.topic, payload=msg.payload, qos=QOS, retain=False)
  except:
    print("unexpected error:", sys.exc_info()[0])

def on_publish(client, userdata, msgid):
    print("message published to remote server - ",msgid)

def on_disconnect_local(client, userdata, rc):
    client.loop_stop()


local_mqttclient = mqtt.Client("TX2")
remote_mqttclient = mqtt.Client("Remote")

local_mqttclient.on_connect = on_connect_local
local_mqttclient.on_subscribe = on_subscribe
remote_mqttclient.on_connect = on_connect_remote

local_mqttclient.on_message = on_message
remote_mqttclient.on_publish = on_publish
local_mqttclient.on_disconnect = on_disconnect_local

local_mqttclient.connect(LOCAL_MQTT_HOST, MQTT_PORT, 600)
local_mqttclient.loop_start()
remote_mqttclient.connect(REMOTE_MQTT_HOST, MQTT_PORT, 600)

remote_mqttclient.loop_forever()  