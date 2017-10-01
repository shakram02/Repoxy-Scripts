import subprocess
import os


class PoxRunner:
    def __init__(self, ip, port, component):
        user_path = os.path.expanduser("~")
        self.command = str("sudo python {}".format(user_path) + "/pox/pox.py" +
                           " openflow.of_01 --address={} ".format(ip) +
                           " --port={} {}".format(port, component) +
                           " info.packet_dump samples.pretty_log log.level --DEBUG")

    def run_pox(self):
        self._process = subprocess.Popen(self.command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

    def shutdown_pox(self):
        import signal
        os.killpg(os.getpgid(self._process.pid), signal.SIGINT)
        self._process.wait()

    def kill_pox(self):
        import signal
        os.killpg(os.getpgid(self._process.pid), signal.SIGKILL)
        self._process.wait()
