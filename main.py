import os
import sys
import paho.mqtt.client as mqtt

from handlers import on_message

broker_url = os.environ['MQTT_BROKER_URL']
broker_port = os.environ['MQTT_BROKER_PORT']

client = mqtt.Client()
client.username_pw_set(username=os.environ['MQTT_USERNAME'],
                       password=os.environ['MQTT_PASSWORD'])

client.connect(broker_url, int(broker_port))


def on_disconnect(_client, _userdata, rc):
    if rc != 0:
        print("Unexpected disconnection. Exiting...")
        sys.exit(1)
    else:
        print("Disconnected successfully")


client.on_message = on_message
client.on_disconnect = on_disconnect

client.subscribe('laseregg')
client.loop_forever()
