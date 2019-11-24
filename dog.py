import datadog
import os

datadog.initialize(api_key=os.environ['DD_API_KEY'],
                   app_key=os.environ['DD_APP_KEY'])

stats = datadog.ThreadStats()
stats.start()


def send(lvl):
    stats.gauge('air.purifier.level', lvl)
