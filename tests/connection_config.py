from enum import Enum  # for enum34, or the stdlib version
import json

with open('config.json') as json_data_file:
    _CONFIG = json.load(json_data_file)


def get_entry(entry_key):
    return _CONFIG[entry_key.value]


class ConfigEntry(Enum):
    ProxyIp = 'proxy_ip'
    ProxyPort = 'proxy_port'


def test():
    print(ConfigEntry.NetworkIp.value, get_entry(ConfigEntry.NetworkIp))


if __name__ == "__main__":
    test()
