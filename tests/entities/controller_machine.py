from entities.pox_runner import PoxRunner
from tcp_channel import TcpClient, TcpServer
from threading import Thread
from time import sleep

KILL_TIMEOUT = 5


class ControllerTx(object):
    """
    Represents an open channel to controller machine
    """

    def __init__(self):
        self._channel = TcpClient()

    def open_connection(self, ip, port):
        self._channel.connect(ip, port)

    def kill_controller(self):
        self._channel.send()


class ControllerMachineRx(object):
    """
    Runs on controller machine to terminate controller software. Upon start the controller
    software will be run automatically, a spinning controller doesn't do any processing nor
    send any packets. So, automatically starting it up just saves effort
    """

    def __init__(self, ip, port):
        self._channel = TcpServer(ip, port)
        self._th = Thread(target=self._recv_thread)
        self._th.start()
        self._pox_runner = PoxRunner(ip, port)

    def _recv_thread(self):
        while True:
            command = self._channel.recv()
            if command is None:
                continue

            if command == "EXIT":
                self.kill_controller()
                self._th.join(5)
                return

    def kill_controller(self):
        self._pox_runner.shutdown_controller()

        if self._pox_runner.is_alive():
            self._force_kill(KILL_TIMEOUT)

    def start_controller(self):
        """
        Called by test maker, not remotely
        :return:
        """
        self._pox_runner.launch_controller()

    def _force_kill(self, timeout=0):
        sleep(timeout)
        if self._pox_runner.is_alive():
            self._pox_runner.kill_controller()
