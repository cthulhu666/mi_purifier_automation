import collections
import json

import miio.airpurifier

import devices
import dog

MIN_LVL = 0
MAX_LVL = 10
DESIRED_PM25 = 5

_devices = devices.all_devices()

_measurements = collections.deque([], 5)


for d in _devices:
    d.set_buzzer(0)
    d.set_mode(miio.airpurifier.OperationMode.Favorite)


def on_message(_client, _userdata, message):
    try:
        data = json.loads(message.payload.decode())
        ts, pm25 = data[0], data[1]['pm25']
        _measurements.append(pm25)
        mean_pm25 = sum(_measurements) / len(_measurements)
        lvl = min(MAX_LVL, round(max(MIN_LVL, mean_pm25 - DESIRED_PM25) / 5))
        print(f"[{ts}] PM2.5: {pm25} (mean: {mean_pm25}) | Setting level: {lvl}")
        for d in _devices:
            if d.status().favorite_level != lvl:
                d.set_favorite_level(lvl)
        dog.send(lvl)
    except Exception as e:
        print(e)
