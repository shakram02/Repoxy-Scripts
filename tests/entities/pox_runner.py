from __future__ import print_function

import os
import shlex
import signal
import subprocess

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
            self._process.wait()
            print(colorize("Shut down controller done exit code {}".format(self._process.returncode)))

            self._process = None
        except Exception as e:
            print(colorize("An error occured while waiting the process to terminate:{}".format(e)))
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
        return self._process is None

    def wait_till_ready(self, on_ready_callback=None):
        """
        Waits until POX has finished starting up
        If you don't want this function to block, pass a callback and run this function in a separate thread
        :param on_ready_callback: function to be called when the controller is ready
        """

        for line in iter(self._process.stderr.readline, b''):
            out_line = line.decode('utf-8')
            print('{0}'.format(out_line))

            # TODO: this is a hack, yes I know. Please tell me if you find a better solution
            if "Listening" in out_line:
                if on_ready_callback is not None:
                    # Callback mode
                    on_ready_callback(out_line)
                else:
                    # Blocking mode
                    return

            if "Error" in out_line:
                return  # TODO report error or recover


BLUE_BACKGROUND_BRIGHT = "\033[0;104m"
WHITE_BOLD = "\033[1;37m"
RESET = "\033[0m"


def colorize(string):
    return "{}{}[{}]{}".format(BLUE_BACKGROUND_BRIGHT, WHITE_BOLD, string, RESET)


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
