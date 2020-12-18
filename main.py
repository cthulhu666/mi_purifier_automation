import os
import sys
import paho.mqtt.client as mqtt

from handlers import on_sensor_msg, on_laseregg_msg, on_button_msg, on_unknown_message

broker_url = os.environ['MQTT_BROKER_URL']  # TODO:rename to MQTT_BROKER_HOST
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


def on_publish(client, userdata, mid):
    print(userdata, mid)


client.message_callback_add('zigbee2mqtt/switch-1', on_button_msg)
client.message_callback_add('zigbee2mqtt/bedroom-sensor-1', on_sensor_msg)
client.message_callback_add('laseregg', on_laseregg_msg)

client.on_message = on_unknown_message
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.subscribe([('laseregg', 0),
                  ('zigbee2mqtt/bedroom-sensor-1', 0),
                  ('zigbee2mqtt/switch-1', 0)])
client.loop_forever()
