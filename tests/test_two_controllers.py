from test_library.automation_functions import *
from test_library.test_machine import TestMachine


def main():
    main_controller = TestMachine(ip="192.168.1.244", messenger_port=6934, controller_port=6834)
    cloned_controller = TestMachine("192.168.1.245", messenger_port=6935, controller_port=6835)

    cloned_controller.start_controller()
    main_controller.start_controller()

    import time
    time.sleep(3)  # Give the controller 3 seconds to start

    network = create_network(proxy_ip="192.168.1.248", proxy_port=6833, switch_count=3)

    start_network(network)
    ping_all(network)
    stop_network(network)

    main_controller.shutdown()
    cloned_controller.shutdown()


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    finally:
        mininet_clean()
