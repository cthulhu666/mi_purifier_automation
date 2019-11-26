import miio.airpurifier
import yaml


def all_devices():
    def device(entry):
        return miio.airpurifier.AirPurifier(entry['ip'],
                                            entry['token'])

    with open('devices.yml', 'r') as f:
        return [(device(e), e) for e in yaml.safe_load(f)['devices']]
