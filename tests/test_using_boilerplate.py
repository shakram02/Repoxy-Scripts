from setup_test_boilerplate import TestBoilerplate
from test_library.automation_functions import *


class TestKilling(TestBoilerplate):
    def __init__(self):
        TestBoilerplate.__init__(self)

    def do_test(self):
        self.setup()
        # Test is now ready

        ping_all(self.network)
        got_feedback = self.wait_feedback_msg()

        stop_network(self.network)

        self.main_controller.shutdown()
        self.cloned_controller.shutdown()


def main():
    tester = TestKilling()
    tester.do_test()


if __name__ == "__main__":
    try:
        main()
    finally:
        mininet_clean()
