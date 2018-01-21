from entities.pox_runner import PoxRunner
from tcp_channel import TcpClient, TcpServer
from threading import Thread
from time import sleep

_KILL_TIMEOUT = 5
_KILL_MSG = "EXIT"


class ControllerTx(object):
    """
    Represents an open channel to controller machine. That's a weak abstraction,
    TODO might be disposed later
    """

    def __init__(self):
        self._channel = TcpClient()

    def open_connection(self, msgr_ip, port):
        self._channel.connect(msgr_ip, port)

    def kill_controller(self):
        self._channel.send(_KILL_MSG)


class ControllerMachineRx(object):
    """
    Runs on controller machine to terminate controller software. Upon start the controller
    software will be run automatically, a spinning controller doesn't do any processing nor
    send any packets. So, automatically starting it up just saves effort
    """

    def __init__(self, msgr_ip, msgr_port):
        self._channel = TcpServer(msgr_ip, msgr_port)
        self._tcp_receiver = Thread(target=self._recv_thread)
        self._tcp_receiver.start()
        self._pox_runner = None

    def _recv_thread(self):
        while True:
            command = self._channel.recv()
            if command is None:
                continue

            if command == _KILL_MSG:
                self.kill_controller()
                self._tcp_receiver.join(5)
                return

    def kill_controller(self):
        self._pox_runner.shutdown_controller()

        if self._pox_runner.is_alive():
            self._force_kill(_KILL_TIMEOUT)

    def start_controller(self, ip, port):
        """
        Called by test maker, not remotely
        :return:
        """
        self._pox_runner = PoxRunner(ip, port)
        self._pox_runner.launch_controller()

    def _force_kill(self, timeout=0):
        sleep(timeout)
        if self._pox_runner.is_alive():
            self._pox_runner.kill_controller()
