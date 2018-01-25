from __future__ import print_function

import os
import shlex
import signal
import subprocess

from entities.networking.utils import colorize
from threading import Timer, Thread

_SHUTDOWN_TIMEOUT = 3


class PoxRunner:
    def __init__(self, ip, port, component="l2_all_to_controller"):
        user_path = os.path.expanduser("~")
        self.command = str("sudo python {}".format(user_path) + "/pox/pox.py" +
                           " openflow.of_01 --address={} ".format(ip) +
                           " --port={} {}".format(port, component) +
                           " info.packet_dump samples.pretty_log log.level --DEBUG")
        self._running = False
        self._process = None

    def launch_controller(self):
        print(colorize("Starting controller"))

        # POX uses stderr for logging
        self._process = subprocess.Popen(shlex.split(self.command), bufsize=0, stderr=subprocess.PIPE)
        print(colorize("Controller started"))

    def shutdown_controller(self):
        if self._process is None:
            return

        try:
            print(colorize("Shutting down controller with [SIGINT],  waiting for termination..."))
            os.kill(self._process.pid, signal.SIGINT)

            # Kill the process after 4 seconds if it didn't terminate, be a daemon, don't annoy us by
            # staying alive
            t = Timer(4, self.kill_controller)
            t.daemon = True
            t.start()

            self._process.wait()
            t.cancel()  # Cancel if everything is fine
            print(colorize("Shut down controller done exit code {}".format(self._process.returncode)))

            if self._process.returncode is not None:
                self._process = None
        except Exception as e:
            print(colorize("An error occured while waiting the process to terminate:{}".format(e)))
            if self.is_alive():
                self.kill_controller()

        print(colorize("Terminated"))
        # TODO confirm controller killed

    def kill_controller(self):
        if self._process is None:
            return

        print(colorize("Killing controller with [SIGKILL]"))
        os.killpg(os.getpgid(self._process.pid), signal.SIGKILL)
        exit_code = self._process.wait()
        print(colorize("Shutting down controller done exit code: {}".format(exit_code)))

    def is_alive(self):
        return self._process is not None

    def wait_till_ready(self, on_ready_callback=None):
        """
        Waits until POX has finished starting up
        If you don't want this function to block, pass a callback and run this function in a separate thread
        :param on_ready_callback: function to be called when the controller is ready
        """

        for line in iter(self._process.stderr.readline, b''):
            out_line = line.decode('utf-8')
            print(out_line)

            # TODO: this is a hack, yes I know. Please tell me if you find a better solution
            # I'm basically scanning stdout for special keywords to know that the controller
            # is ready
            if "Listening" in out_line:
                out_printer = Thread(target=self._keep_printing_output)
                out_printer.daemon = True
                out_printer.start()
                if on_ready_callback is not None:
                    # Callback mode
                    on_ready_callback(out_line)
                else:
                    # Blocking mode
                    return

            if "Error" in out_line:
                return  # TODO report error or recover

    def _keep_printing_output(self):
        try:
            for line in iter(self._process.stderr.readline, b''):
                print(line.decode('utf-8'))
        except AttributeError:
            print(colorize("Process is now killed, will no longer print std stream outputs"))


def on_ready(x):
    print("READY:", x)


def test():
    # Start POX then tear it down
    runner = PoxRunner("localhost", 6833)
    runner.launch_controller()

    runner.wait_till_ready()
    print("Waiting till shutdown...")
    runner.shutdown_controller()


if __name__ == "__main__":
    test()
