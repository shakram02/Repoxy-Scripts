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

        # Those 2 operations are blocking, they need to be performed on separate threads
        self.watch_for_message(self.on_receivce_feedback)
        ping_all(self.network)

        got_feedback = self.wait_for_feedback_message()

        if not got_feedback:
            logging.warn("[Failed to get controller feedback]")

        stop_network(self.network)

        # self.main_controller.shutdown()
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
