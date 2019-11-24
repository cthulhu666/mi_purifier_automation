import os
import paho.mqtt.client as mqtt

from handlers import on_message

broker_url = "farmer.cloudmqtt.com"
broker_port = 12397

client = mqtt.Client()
client.username_pw_set(username=os.environ['MQTT_USERNAME'],
                       password=os.environ['MQTT_PASSWORD'])

client.connect(broker_url, broker_port)

client.on_message = on_message
client.subscribe('laseregg')
client.loop_forever()
