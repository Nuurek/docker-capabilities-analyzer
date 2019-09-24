# read the input
# start the container
# get container's pid and declared capabilities
# trace fork -> update children pids
# trace kill -> update children pids
# trace capable -> check if in pids and add cap to set
import signal
import uuid

import docker
from docker.models.containers import Container

from capabilites import Capabilities, DEFAULT_CAPABILITIES
from parser import Parser

args = Parser.get_arguments()

TRACED_CONTAINER_NAME_PREFIX: str = 'traced'
container_name: str = f'{TRACED_CONTAINER_NAME_PREFIX}_{uuid.uuid4()}'

client: docker.DockerClient = docker.from_env()

parameters = {
    'name': container_name,
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


def signal_handler(_signal_number, _frame):
    clean_up()


def clean_up():
    print('Stopping container')
    container.stop()
    print('Stopped container')
    print('Removing container')
    container.remove()
    print('Removed container')


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

try:
    container.wait()
except KeyboardInterrupt:
    clean_up()
