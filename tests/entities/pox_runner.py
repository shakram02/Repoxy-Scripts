import subprocess
import os
import signal
from logging import debug
from threading import Thread
import shlex

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
        debug(colorize("Starting controller"))
        # self._process = subprocess.Popen(self.command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        self._process = subprocess.Popen(shlex.split(self.command), bufsize=0,
                                         universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        debug(colorize("Controller started"))

    def shutdown_controller(self, timeout=_SHUTDOWN_TIMEOUT):
        if self._process is None:
            return
        debug(colorize("Shutting down controller with [SIGINT],  waiting for termination..."))

        os.killpg(os.getpgid(self._process.pid), signal.SIGINT)
        try:
            self._process.wait(timeout)
            self._process = None

            debug(colorize("Terminated"))
        except Exception as e:
            debug(colorize("An error occured while waiting the process to terminate:{}".format(e)))
            self.kill_controller()

        debug(colorize("Shut down controller done exit code"))

    def kill_controller(self):
        if self._process is None:
            return

        debug(colorize("Killing controller with [SIGKILL]"))
        os.killpg(os.getpgid(self._process.pid), signal.SIGKILL)
        exit_code = self._process.wait()
        debug(colorize("Shutting down controller done exit code: {}".format(exit_code)))

    def is_alive(self):
        return self._process is None

    def read_stdout(self):
        for line in iter(self._process.stdout.readline, b''):
            print('got line: {0}'.format(line.decode('utf-8')))


BLUE_BACKGROUND_BRIGHT = "\033[0;104m"
WHITE_BOLD = "\033[1;37m"
RESET = "\033[0m"


def colorize(string):
    return "{}{}[{}]{}".format(BLUE_BACKGROUND_BRIGHT, WHITE_BOLD, string, RESET)


def test():
    runner = PoxRunner("localhost", 6833)
    runner.launch_controller()

    th = Thread(target=runner.read_stdout)
    th.start()

    th.join()
    from time import sleep
    print("Waiting till shutdown...")
    sleep(7)
    runner.shutdown_controller()


if __name__ == "__main__":
    test()
