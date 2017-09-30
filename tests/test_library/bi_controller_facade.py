from automation_functions import *
from test_machine import TestMachine


class BiControllerFacade:
    BLUE_BACKGROUND_BRIGHT = "\033[0;104m"
    WHITE_BOLD = "\033[1;37m"
    RESET = "\033[0m"

    def __init__(self):
        mininet_clean()
        self.main_controller = TestMachine(ip="192.168.1.244", messenger_port=6934, controller_port=6834)
        self.cloned_controller = TestMachine("192.168.1.245", messenger_port=6935, controller_port=6835)
        self._log("Ready to go")

    def start_controllers(self):
        self._log("Starting controllers")
        self.cloned_controller.start_controller()
        self.main_controller.start_controller()
        self._log("Giving sometime for controllers to start")
        import time
        time.sleep(0.3)  # Give the controller 300ms to start
        self._log("Done waiting")

    def stop_controllers(self):
        self.cloned_controller.stop_controller()
        self.main_controller.stop_controller()
        self._log("Stopped controllers")

    def create_and_start_network(self):
        self.network = create_network(proxy_ip="192.168.1.248", proxy_port=6833, switch_count=3)
        start_network(self.network)

    def stop_network(self):
        stop_network(self.network)

    def ping_all(self):
        ping_all(self.network)

    def end_test(self):
        self.main_controller.shutdown()
        self.cloned_controller.shutdown()
        mininet_clean()

    @staticmethod
    def _log(string):
        print "{}{}[{}]{}".format(BiControllerFacade.BLUE_BACKGROUND_BRIGHT, BiControllerFacade.WHITE_BOLD,
                                  string, BiControllerFacade.RESET)
