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


for d, _ in _devices:
    d.set_buzzer(0)
    d.set_mode(miio.airpurifier.OperationMode.Favorite)


def on_message(_client, _userdata, message):
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


def _calculate_level(mean_pm25, leniency):
    lvl = round((mean_pm25 - DESIRED_PM25) / leniency)
    return min(MAX_LVL, max(MIN_LVL, lvl))
