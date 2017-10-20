from test_library.automation_functions import *
from test_library.test_machine import TestMachine
from test_library.messenger.controller_feedback_listener import ControllerFeedbackListener
from threading import Thread, Event

from logging import warn, debug, ERROR, DEBUG, error

_CONNECTION_TIMEOUT = 15


class ProcessWaiter:
    def __init__(self, event_obj):
        self._event_obj = event_obj  # Event object
        self._success = False

    @property
    def is_success(self):
        return self._success


class ControllerWaiter(ProcessWaiter):
    def __init__(self, listener_ip, listener_port, completition_event):
        ProcessWaiter.__init__(self, completition_event)
        # Open the listening socket
        self._feedback_listener = ControllerFeedbackListener(listener_ip, listener_port)
        debug("[Listening socket is now open]")

    def start(self):
        try:

            # Wait for the controller to connect
            client_addr = self._feedback_listener.accept_client(_CONNECTION_TIMEOUT)  # Wait for controller to go up
            debug("[Controller connected:" + str(client_addr) + "]")
            self._success = True

        except Exception as e:
            error("[Failed to obtain connection {}]".format(e))

        # Notify the main thread for completion
        self._event_obj.set()

    @property
    def listener(self):
        return self._feedback_listener


class FeedbackWaiter(ProcessWaiter):
    def __init__(self, feedback_listener, start_event_obj, event_obj):
        ProcessWaiter.__init__(self, event_obj)
        self._feedback_listener = feedback_listener
        self._started_event = start_event_obj

    def start(self, on_completion):
        try:

            debug("[Waiting for controller message]")
            self._started_event.set()
            msg = self._feedback_listener.wait_for_message(_CONNECTION_TIMEOUT)
            # The message should be sent with the first PacketIn
            debug("[Received \"{}\"]".format(msg))
            on_completion(msg)
            self._success = True

        except Exception as e:
            error("Failed to get controller message:{}".format(e))

        # Notify the main thread for completion
        self._event_obj.set()


class TestBoilerplate:
    def __init__(self, listener_ip="192.168.1.241", listener_port=6931):
        self.main_controller = TestMachine(ip="192.168.1.244", messenger_port=6934, controller_port=6834)
        self.cloned_controller = TestMachine("192.168.1.245", messenger_port=6935, controller_port=6835)
        self._listener_ip = listener_ip
        self._listener_port = listener_port
        self._feedback_listener = None

    def setup(self):
        controller_connect_event = Event()
        controller_waiter = ControllerWaiter(self._listener_ip, self._listener_port, controller_connect_event)

        # Start controller waiter
        wait_thread = Thread(target=controller_waiter.start)
        wait_thread.setDaemon(True)
        wait_thread.start()

        # Start controllers
        self.cloned_controller.start_controller()
        self.main_controller.start_controller()

        controller_connect_event.wait()
        if not controller_waiter.is_success:
            raise RuntimeError("Couldn't get controller connection")

        self._feedback_listener = controller_waiter.listener
        self.network = create_network(proxy_ip="192.168.1.248", proxy_port=6833, switch_count=4)
        start_network(self.network)

        # Start feedback waiter
        self.feedback_ready_event = Event()

    def do_test(self):
        raise NotImplementedError()
        pass

    def watch_for_message(self, on_completion):
        started_event = Event()
        self.message_waiter = FeedbackWaiter(self._feedback_listener, started_event, self.feedback_ready_event)

        # Pinging the network is blocking, and waiting for the controller is blocking also
        # there 2 processes need to be done on separate thereads
        wait_thread = Thread(target=self.message_waiter.start, args=[on_completion])
        wait_thread.setDaemon(True)
        wait_thread.start()
        started_event.wait()
        debug("[Watcher launched]")

    def wait_for_feedback_message(self, timeout=_CONNECTION_TIMEOUT):
        # Wait either for completion or timeout
        wait_result = self.feedback_ready_event.wait(timeout=timeout)

        if not wait_result:
            raise RuntimeError("Couldn't get controller message, [TIMEOUT]")

        return self.message_waiter.is_success
