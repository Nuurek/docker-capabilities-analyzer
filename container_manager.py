from argparse import Namespace
from typing import Dict

import docker
from docker.models.containers import Container


class ContainerManager:
    STATE_ATTRIBUTE_KEY = 'State'
    PROCESS_ID_STATE_KEY = 'Pid'
    HOST_CONFIG_ATTRIBUTE_KEY = 'HostConfig'

    _container: Container

    def __init__(self):
        # Use the environment configuration for Docker client
        self._client: docker.DockerClient = docker.from_env()

    def start(self, args: Namespace) -> int:
        parameters = self._get_parameters(args)

        # Container will be created but not started instantly
        # To actually read the container's process id client has to reload the object
        print('Starting container')
        self._container: Container = self._client.containers.run(**parameters)
        container_pid = self._wait_for_container_pid()
        print('Started container:', self._container.name)

        return container_pid

    def get_config(self) -> Dict:
        return self._container.attrs[self.HOST_CONFIG_ATTRIBUTE_KEY]

    def logs(self):
        # Return iterable with STDOUT and STDERR
        return self._container.logs(stream=True)

    def stop(self):
        print('Stopping container')
        self._container.stop()
        print('Stopped container')

        print('Removing container')
        self._container.remove()
        print('Removed container')

    @staticmethod
    def _get_parameters(args: Namespace) -> Dict:
        return {
            'name': args.name,
            'image': args.image,
            'detach': True,
            'environment': args.env,
            'ports': args.publish,
            'volumes': args.volume,
            'cap_add': args.cap_add,
            'cap_drop': args.cap_drop,
            'privileged': bool(args.privileged)
        }

    def _wait_for_container_pid(self) -> int:
        # Reload the container object until it has its process id set
        container_pid = None
        while not container_pid:
            self._container.reload()
            container_pid: int = self._container.attrs[self.STATE_ATTRIBUTE_KEY][self.PROCESS_ID_STATE_KEY]

        return container_pid
