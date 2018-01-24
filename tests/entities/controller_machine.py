from threading import Thread
from time import sleep

from entities.networking.tcp_channel import TcpServer, TcpClient
from entities.networking.utils import get_ip, colorize
from entities.pox_runner import PoxRunner
from entities.protocol import SERVER_PORT, CONTROLLER_READY, KILL_MSG


class ControllerTx(object):
    """
    Represents an open channel to controller machine. That's a weak abstraction,
    TODO might be disposed later
    """

    def __init__(self, client_socket):
        self._socket = client_socket

    def wait_ready(self):
        return self._socket.recv(256)

    def kill_controller(self):
        self._socket.send(KILL_MSG)
        self._socket.close()


class ControllerMachineRx(object):
    """
    Runs on controller machine to terminate controller software. Upon start the controller
    software will be run automatically, a spinning controller doesn't do any processing nor
    send any packets. So, automatically starting it up just saves effort
    """

    def __init__(self, server_ip, server_port, on_controller_ready=None):
        """
        Creates a new instance of controller process manager
        :param server_ip: IP of the network server that's opening the TCP listening socket
        :param server_port: Port of the TCP socket
        :param on_controller_ready: Callback function if we won't block until controller is ready
        """
        self._channel = TcpClient()
        self._on_ready = on_controller_ready
        self._server_ip = server_ip
        self._server_port = server_port

        self._pox_runner = None
        self._temp_th_wait_ready = None

    def wait_till_terminate_requested(self):
        command = self._channel.recv()  # Returns None for some reason
        if command is not None:
            print(colorize("Rx... {}".format(command)))
        else:
            print(colorize("Rx..."))

        if command == KILL_MSG:
            print(colorize("Killing controller"))
            self._kill_controller()
            return

    def _kill_controller(self):
        self._pox_runner.shutdown_controller()
        self._channel.close()

        if self._pox_runner.is_alive():
            self._force_kill()

    def start_controller(self, ip, port):
        """
        Called by test maker, not remotely.
        Will block until the controller is ready
        :param ip Controller IP
        :param port Controller port
        """

        self._pox_runner = PoxRunner(ip, port)
        self._pox_runner.launch_controller()
        if self._on_ready is not None:
            # Don't block
            self._temp_th_wait_ready = Thread(target=self._pox_runner.wait_till_ready, args=(self._on_ready,))
            self._temp_th_wait_ready.daemon = True
            self._temp_th_wait_ready.start()
        else:
            # Block
            self._pox_runner.wait_till_ready()
            self._channel.send(CONTROLLER_READY)

    def wait_ready_thread(self):
        """
        Blocks until the thread waitining the controller to be ready finishes
        :return:
        """
        if self._temp_th_wait_ready is None:
            return
        else:
            self._temp_th_wait_ready.join()

        self._channel.send(CONTROLLER_READY)

    def connect_to_command_server(self):
        # Initialize conenction with the other end point
        self._channel.connect(self._server_ip, self._server_port)

    def _force_kill(self):
        if self._pox_runner.is_alive():
            self._pox_runner.kill_controller()


def _serv_thread():
    client_count = 1
    tcp_server = TcpServer(get_ip(), SERVER_PORT)

    txs = []
    for i in range(client_count):
        print("Waiting to accept...")
        sock = tcp_server.accept()
        print("Accepted client...")
        tx = ControllerTx(sock)
        txs.append(tx)

    for tx in txs:
        print("Waiting controller to be ready...")
        tx.wait_ready()

    print("Controllers ready...")

    for tx in txs:
        tx.kill_controller()


def test():
    th = Thread(target=_serv_thread)
    th.daemon = True

    th.start()
    sleep(1)

    machine = ControllerMachineRx(get_ip(), SERVER_PORT)
    print("Trying to connect...")
    machine.connect_to_command_server()

    machine.start_controller(get_ip(), 6834)

    th.join()


if __name__ == "__main__":
    test()
