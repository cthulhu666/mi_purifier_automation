import collections
import json

import miio.airpurifier

import devices
import dog

MIN_LVL = 0
MAX_LVL = 10
DESIRED_PM25 = 5
DEFAULT_LENIENCY = 5

_devices = devices.all_devices()

_measurements = collections.deque([], 5)


# for d, _ in _devices:
#     d.set_buzzer(0)
#     d.set_mode(miio.airpurifier.OperationMode.Favorite)


def on_sensor_msg(_client, _userdata, message):
    data = json.loads(message.payload.decode())
    device = message.topic.split('/')[1]
    print(device, data)
    tags = [f"device:{device}"]
    for k in ['humidity', 'temperature', 'battery', 'linkquality']:
        dog.gauge(f'sensor.{k}', data.get(k), tags)


def on_laseregg_msg(_client, _userdata, message):
    try:
        data = json.loads(message.payload.decode())
        ts, pm25 = data[0], data[1]['pm25']
        _measurements.append(pm25)
        mean_pm25 = sum(_measurements) / len(_measurements)
        print(f"[{ts}] PM2.5: {pm25} (mean: {mean_pm25})")
        for d, cfg in _devices:
            leniency = cfg.get('leniency', DEFAULT_LENIENCY)
            lvl = _calculate_level(mean_pm25, leniency)
            if d.status().favorite_level != lvl:
                print(f"{cfg['name']} | Adjusting level: {lvl}")
                d.set_favorite_level(lvl)
            else:
                print(f"{cfg['name']} | Keeping level: {lvl}")
            dog.send(cfg['name'], lvl)
    except Exception as e:
        print(e)


def on_button_msg(client, _userdata, message):
    data = json.loads(message.payload.decode())
    # each click seems to generate two very similar messages
    # one with `action` and the other with `click` attribute in payload
    # let's ignore one.
    if 'action' not in data:
        return
    print("on_button_msg", data)
    action = data['action']
    if action == 'single':
        client.publish('zigbee2mqtt/bathroom-1-light/set',
                       json.dumps({'state_left': 'on', 'state_right': 'on'}))
    if action == 'double':
        client.publish('zigbee2mqtt/bathroom-1-light/set',
                       json.dumps({'state_left': 'off', 'state_right': 'off'}))


def on_unknown_message(_client, _userdata, message):
    print(f"Unknown topic: {message.topic}")


def _calculate_level(mean_pm25, leniency):
    lvl = round((mean_pm25 - DESIRED_PM25) / leniency)
    return min(MAX_LVL, max(MIN_LVL, lvl))
