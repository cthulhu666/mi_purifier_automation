import datadog
import os

datadog.initialize(api_key=os.environ['DD_API_KEY'],
                   app_key=os.environ['DD_APP_KEY'])

stats = datadog.ThreadStats()
stats.start()


def gauge(metric_name, value, tags):
    stats.gauge(metric_name, value, tags=tags)


# TODO: remove
def send(device: str, lvl: int):
    stats.gauge('air.purifier.level', lvl, tags=[f"device:{device.lower()}"])
