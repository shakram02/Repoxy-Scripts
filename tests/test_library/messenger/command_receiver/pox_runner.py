import subprocess
import os
import signal
from logging import debug
from misc import colorize

_SHUTDOWN_TIMEOUT = 3


class PoxRunner:
    def __init__(self, ip, port, component="l2_all_to_controller"):
        user_path = os.path.expanduser("~")
        self.command = str("sudo python {}".format(user_path) + "/pox/pox.py" +
                           " openflow.of_01 --address={} ".format(ip) +
                           " --port={} {}".format(port, component) +
                           " info.packet_dump samples.pretty_log log.level --DEBUG")
        self._running = False

    def launch_controller(self):
        debug(colorize("Starting controller"))
        self._process = subprocess.Popen(self.command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        debug(colorize("Controller started"))

    def shutdown_controller(self, timeout=_SHUTDOWN_TIMEOUT):
        os.killpg(os.getpgid(self._process.pid), signal.SIGINT)

        debug(colorize("Shutting down controller with [SIGINT]"))
        try:
            self._process.wait()
        except Exception as e:
            debug(colorize("An error occured while waiting the process to terminate:{}".format(e)))

        debug(colorize("Shut down controller done exit code"))

    def kill_controller(self):
        debug(colorize("Killing controller with [SIGINT]"))
        os.killpg(os.getpgid(self._process.pid), signal.SIGKILL)
        exit_code = self._process.wait()
        debug(colorize("Shutting down controller done exit code: {}".format(exit_code)))
