from time import sleep
from threading import Thread, Event
import shlex
import re
import subprocess
import sys

BLUE_BACKGROUND_BRIGHT = "\033[0;104m"
WHITE_BOLD = "\033[1;37m"
RESET = "\033[0m"


def colorize(string):
    return "{}{}[{}]{}".format(BLUE_BACKGROUND_BRIGHT, WHITE_BOLD, string, RESET)


class CbenchResult(object):
    # ['1', '3', '452.97', '514.00', '481.99', '25.00']
    def __init__(self, result_list):
        self.switches, self.tests, self.min_res, self.max_res, self.avg, self.stddev = tuple(result_list)

    def __str__(self):
        return "Switches:{} Tests:{} Min:{} Max:{} Average:{} StdDev:{}".format(self.switches, self.tests, self.min_res,
                                                                                self.max_res, self.avg, self.stddev)

    def __repr__(self):
        return self.__str__()


class DotSpinner(object):

    def __init__(self):
        self._t = None
        self._pill = Event()

    def _print_dot(self):
        while not self._pill.is_set():
            sys.stdout.write(".")
            sys.stdout.flush()
            sleep(0.5)

        sys.stdout.write('\n')
        sys.stdout.flush()

    def start(self):
        self._t = Thread(target=self._print_dot)
        self._t.daemon = True
        self._t.start()

    def stop(self):
        self._pill.set()
        self._t.join()


def run(ip, port, loops, switches, warmup=2):
    spinner = DotSpinner()

    command = str("cbench -c {} -p {} -D 2000 -s {} -w {} -l {}".format(ip, port, switches, warmup, loops))
    process = subprocess.Popen(shlex.split(command), bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    spinner.start()
    result = None

    # Put reader on another thread
    for line in iter(process.stdout.readline, b''):
        out_line = line.decode('utf-8')

        # RESULT: 1 switches 3 tests min/max/avg/stdev = 452.97/514.00/481.99/25.00 responses/s
        if "RESULT" not in out_line:
            continue

        out_line = out_line.strip()
        result = re.findall("\d+[.,]?\d*", out_line)
        break

    process.wait()
    spinner.stop()

    if result is None:
        # Convert the error log to a human readable string.
        return "".join([x.decode() for x in process.stderr.readlines()])

    return CbenchResult(result)


def test():
    ip = "192.168.1.244"
    port = 6834
    loops = 5

    print(colorize("Cbench started, waiting..."))
    print(colorize(run(ip, port, loops, 1)))


if __name__ == "__main__":
    test()
