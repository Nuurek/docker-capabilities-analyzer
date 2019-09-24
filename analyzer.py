# build from source
# go to bcc/build/src/python/bcc-python
# pip install .

# read the input
# start the container
# get container's pid and declared capabilities
# trace fork -> update children pids
# trace kill -> update children pids
# trace capable -> check if in pids and add cap to set
import signal
import sys
from threading import Event

import docker
from docker.models.containers import Container

from cap_capable_tracer import CapCapableTracer
from capabilites import Capabilities, DEFAULT_CAPABILITIES
from parser import Parser

args = Parser.get_arguments()

client: docker.DockerClient = docker.from_env()

parameters = {
    'name': args.name,
    'image': args.image,
    'detach': True,
    'environment': args.env,
    'ports': args.publish,
    'volumes': args.volume,
    'cap_add': args.cap_add,
    'cap_drop': args.cap_drop
}

print('Running container')
container: Container = client.containers.run(**parameters)
print('Ran container')

container_pid = container.attrs['State']['Pid']
while container_pid == 0:
    print('reloading')
    container.reload()
    container_pid = container.attrs['State']['Pid']

host_config = container.attrs['HostConfig']
added_capabilities = Capabilities.from_strings(host_config['CapAdd'])
dropped_capabilities = Capabilities.from_strings(host_config['CapDrop'])

capabilities = DEFAULT_CAPABILITIES.union(added_capabilities).difference(dropped_capabilities)

finish_event = Event()

cap_capable_tracer = CapCapableTracer(container_pid, finish_event)
cap_capable_tracer.start()


def clean_up():
    finish_event.set()
    cap_capable_tracer.stop()

    print('Stopping container')
    container.stop()
    print('Stopped container')
    print('Removing container')
    container.remove()
    print('Removed container')

    sys.exit()


def signal_handler(_signal_number, _frame):
    print('signal_handler', _signal_number)
    clean_up()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

container.wait()
clean_up()
