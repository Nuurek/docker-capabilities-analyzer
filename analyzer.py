import signal
import sys
from threading import Event

import docker
from docker.models.containers import Container

from cap_capable_tracer import CapCapableTracer
from capabilites import Capabilities, DEFAULT_CAPABILITIES
from container_manager import ContainerManager
from parser import Parser

args = Parser.get_arguments()

container_manager = ContainerManager()
container_pid = container_manager.run(args)

# host_config = container.attrs['HostConfig']
# added_capabilities = Capabilities.from_strings(host_config['CapAdd'])
# dropped_capabilities = Capabilities.from_strings(host_config['CapDrop'])
#
# capabilities = DEFAULT_CAPABILITIES.union(added_capabilities).difference(dropped_capabilities)

cap_capable_tracer = CapCapableTracer(container_pid)
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
