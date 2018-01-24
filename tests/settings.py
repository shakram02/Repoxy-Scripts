import json
import os
from enum import Enum  # for enum34, or the stdlib version

file_path = os.path.join(os.path.dirname(__file__))

with open(os.path.join(file_path, 'config.json')) as json_data_file:
    _CONFIG = json.load(json_data_file)


def get_entry(entry_key):
    return _CONFIG[entry_key.value]


class ConfigEntry(Enum):
    NetworkIp = 'network_ip'

    ProxyIp = 'proxy_ip'
    ProxyPort = 'proxy_port'

    MainControllerIp = 'cont_main_ip'
    ReplicatedControllerIp = 'cont_repl_ip'


def test():
    print(ConfigEntry.NetworkIp.value, get_entry(ConfigEntry.NetworkIp))


if __name__ == "__main__":
    test()
