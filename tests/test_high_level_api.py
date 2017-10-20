from test_library.bi_controller_facade import BiControllerFacade
from test_library.automation_functions import mininet_clean


def main():
    test_obj = BiControllerFacade()

    test_obj.start_controllers()

    import time
    time.sleep(0.5)

    test_obj.create_network()
    test_obj.start_network()
    test_obj.ping_all()

    test_obj.stop_network()

    test_obj.stop_controllers()


if __name__ == "__main__":
    try:
        main()
    finally:
        mininet_clean()
