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
import uuid
from threading import Thread, Event

import docker
from bcc import BPF
from docker.models.containers import Container

from capabilites import Capabilities, DEFAULT_CAPABILITIES
from parser import Parser

args = Parser.get_arguments()

TRACED_CONTAINER_NAME_PREFIX: str = 'traced'
container_name: str = f'{TRACED_CONTAINER_NAME_PREFIX}_{uuid.uuid4()}'

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

host_config = container.attrs['HostConfig']
added_capabilities = Capabilities.from_strings(host_config['CapAdd'])
dropped_capabilities = Capabilities.from_strings(host_config['CapDrop'])

capabilities = DEFAULT_CAPABILITIES.union(added_capabilities).difference(dropped_capabilities)

b = BPF(src_file='trace_capable.c')


def print_event(_core, data, _size):
    event = b["events"].event(data)
    capability = Capabilities(event.cap)
    print(event.pid, capability)


b["events"].open_perf_buffer(print_event)


finished = Event()


def poll_capable_kernel():
    while not finished.is_set():
        b.perf_buffer_poll()


thread = Thread(None, poll_capable_kernel)
thread.start()


def clean_up():
    finished.set()
    thread.join()

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
