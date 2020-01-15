import os
import paho.mqtt.client as mqtt

from handlers import on_message

broker_url = "farmer.cloudmqtt.com"
broker_port = 12397

client = mqtt.Client()
client.username_pw_set(username=os.environ['MQTT_USERNAME'],
                       password=os.environ['MQTT_PASSWORD'])

client.connect(broker_url, broker_port)


def on_disconnect(_client, _userdata, rc):
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")


client.on_message = on_message
client.on_disconnect = on_disconnect

client.subscribe('laseregg')
client.loop_forever()
