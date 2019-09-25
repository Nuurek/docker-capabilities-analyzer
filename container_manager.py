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
        self._client: docker.DockerClient = docker.from_env()

    def start(self, args: Namespace):
        parameters = self._get_parameters(args)

        print('Starting container')
        self._container: Container = self._client.containers.run(**parameters)
        print('Started container:', self._container.name)

        container_pid = self._wait_for_container_pid()

        return container_pid

    def get_config(self) -> Dict:
        return self._container.attrs[self.HOST_CONFIG_ATTRIBUTE_KEY]

    def wait(self):
        self._container.wait()
        return self._container.logs()

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
            'cap_drop': args.cap_drop
        }

    def _wait_for_container_pid(self):
        container_pid = None
        while not container_pid:
            print('Reloading container')
            self._container.reload()
            container_pid = self._container.attrs[self.STATE_ATTRIBUTE_KEY][self.PROCESS_ID_STATE_KEY]

        return container_pid
