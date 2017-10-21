import logging

from setup_test_boilerplate import TestBoilerplate
from test_library.automation_functions import *


class TestKilling(TestBoilerplate):
    def __init__(self):
        TestBoilerplate.__init__(self)

    def on_receivce_feedback(self, msg):
        logging.debug("[Received controller feedback]")
        self.main_controller.shutdown()
        logging.debug("Turned off main controller]")

    def do_test(self):
        self.setup()
        # Test is now ready

        # Main controller will go down after first non-arp packet
        ping_all(self.network)

        stop_network(self.network)
        self.cloned_controller.shutdown()


def main():
    tester = TestKilling()
    tester.do_test()


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        main()
    finally:
        mininet_clean()
