from test_library.automation_functions import *
from test_library.test_machine import TestMachine
from test_library.messenger.controller_feedback_listener import ControllerFeedbackListener


def wait_for_client(feedback_listener):
    try:
        client_addr = feedback_listener.wait_for_client()  # Wait for controller to go up
    except Exception as e:
        import sys
        print (e)
        sys.exit(-1)
    print("Client connected:" + str(client_addr))


def send_kill_when_ready(main_controller, feedback_listener):
    msg = feedback_listener.wait_for_message()

    # The message ("UP") is defined in the controller component
    # The message should be sent with the first PacketIn
    if msg == "UP":
        main_controller.kill_controller()
        feedback_listener.close_connection()
        print("[Received ready message]")
    else:
        raise ValueError("Invalid message {}" % msg)


def main():
    main_controller = TestMachine(ip="192.168.1.244", messenger_port=6934, controller_port=6834)
    cloned_controller = TestMachine("192.168.1.245", messenger_port=6935, controller_port=6835)

    listener_ip = "192.168.1.241"
    listener_port = 6931
    feedback_listener = ControllerFeedbackListener(listener_ip, listener_port, timeout=30)
    feedback_listener.start_listening()

    from threading import Thread
    client_acceptor = Thread(target=wait_for_client, args=[feedback_listener])
    client_acceptor.setDaemon(True)
    client_acceptor.start()

    cloned_controller.start_controller()
    main_controller.start_controller()

    # Connect to the proxy
    network = create_network(proxy_ip="192.168.1.248", proxy_port=6833)

    start_network(network)

    print("Thread state:" + str(client_acceptor.isAlive()))
    if client_acceptor.isAlive():
        print("Waiting for client acceptor")
        client_acceptor.join()

    message_handler = Thread(target=send_kill_when_ready, args=[main_controller, feedback_listener])
    message_handler.setDaemon(True)
    message_handler.start()

    ping_all(network)
    stop_network(network)

    main_controller.shutdown()
    cloned_controller.shutdown()

    if message_handler.isAlive():
        print("Waiting for message handler")
        message_handler.join()


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    finally:
        mininet_clean()
