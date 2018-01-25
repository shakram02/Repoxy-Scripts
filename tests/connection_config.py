from enum import Enum  # for enum34, or the stdlib version
import os
import json

file_path = os.path.join(os.path.dirname(__file__))

with open(os.path.join(file_path, 'config.json')) as json_data_file:
    _CONFIG = json.load(json_data_file)


def get_entry(entry_key):
    if isinstance(entry_key, str):
        return _CONFIG[entry_key]
    else:
        return _CONFIG[entry_key.value]


class ConfigEntry(Enum):
    ProxyIp = 'proxy_ip'
    ProxyPort = 'proxy_port'


def test():
    print(ConfigEntry.ProxyIp.value, get_entry(ConfigEntry.ProxyIp))


if __name__ == "__main__":
    test()
