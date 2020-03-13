import paho.mqtt.client as mqtt
import time
import datetime

LOCAL_MQTT_HOST="172.18.0.2"  # "iot.eclipse.org" #"mosquitto"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="test_topic"
count = 0
def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	
#def on_message(client,userdata, msg):
#  try:
#    print("message received!")	
    # if we wanted to re-publish this message, something like this should work
    # msg = msg.payload
    # remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
#  except:
#    print("Unexpected error:", sys.exc_info()[0])

def on_publish(client,userdate,mid):
    print(str(count) + ": Face Published")

def publish_message(client):
    client.publish("tx2/face", str(count)+":"+str(datetime.datetime.now()), qos=0)
    time.sleep(1)

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_publish = on_publish



# go into a loop
#local_mqttclient.loop_forever()

while True:
     publish_message(local_mqttclient)
     count += 1