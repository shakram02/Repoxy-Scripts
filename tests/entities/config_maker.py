from entities.networking.utils import get_ip


class ConfigMaker(object):

    def __init__(self, controller_port):
        self._controller_port = controller_port
        self._ip = get_ip()

    def get_broadcast_msg(self):
        return "{}_{}".format(self._ip, self._controller_port)

    def get_ip(self):
        return self._ip

    def get_controller_port(self):
        return self._controller_port
