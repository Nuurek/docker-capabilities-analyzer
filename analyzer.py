import signal
import sys

from cap_capable_tracer import CapCapableTracer
from container_manager import ContainerManager
from parser import Parser

args = Parser.get_arguments()

container_manager = ContainerManager()

container_pid = container_manager.start(args)
config = container_manager.get_config()

cap_capable_tracer = CapCapableTracer(container_pid, config)
cap_capable_tracer.start()


def clean_up():
    cap_capable_tracer.stop()

    container_manager.stop()

    sys.exit()


def signal_handler(_signal_number, _frame):
    clean_up()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

container_manager.wait()
clean_up()
