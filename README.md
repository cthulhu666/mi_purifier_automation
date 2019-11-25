# Mi Air Purifier Automation

This is a simple script that adjusts `favorite_level` on Mi Purifier devices<br />
according to pm25 measurements delivered via MQTT topic.

In my case, measurements are recorder by a Laser Egg device.

The formula for `favorite_level` is:
```
min(MAX_LVL, round(max(MIN_LVL, mean_pm25 - DESIRED_PM25) / 5))
```
where `MAX_LVL` is 10,<br/>
`MIN_LVL` is 0,<br/>
`DESIRED_PM25` is 5<br/>
and `mean_pm25` is average from last 5 measurements.

## Configuration

Environment variables

* MQTT_USERNAME
* MQTT_PASSWORD
* DD_API_KEY
* DD_APP_KEY

( self explanatory, I hope )

You also need `devices.yml`, here's a sample:

```yaml
devices:
  - name: Office
    ip: 192.168.1.100
    token: xxxxxxxxxxxxx
  - name: Bedroom
    ip: 192.168.1.101
    token: xxxxxxxxxxxxx

```

## MQTT subscriber

This app subscribes to `laseregg` topic, 
and it expects messages with following schema:
```
[<timestamp>, {'pm25': <measurement>}]
```

Timestamp is only for debugging purposes.

## TODO

* make DataDog optional
* make MQTT broker host/port configurable
* make MQTT topic name
* improve message schema
* make formula configurable (at least MAX_LVL and DESIRED_PM25 parameters)
* introduce 'night mode' (switching to silent mode or just decreasing `favorite_level`)
