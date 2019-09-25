from argparse import ArgumentParser, Namespace, Action
from typing import Dict, List


class Parser:
    class PublishAction(Action):
        def __call__(self, parser: ArgumentParser, namespace: Namespace, value: str, option_string: str = None):
            host_port, container_port = value.split(':')
            ports: Dict[str, str] = getattr(namespace, self.dest) or {}
            ports = {
                **ports,
                container_port: host_port
            }
            setattr(namespace, self.dest, ports)

    class VolumeAction(Action):
        def __call__(self, parser: ArgumentParser, namespace: Namespace, value: str, option_string: str = None):
            host_source, container_destination = value.split(':')
            volumes: Dict[str, Dict[str, str]] = getattr(namespace, self.dest) or {}
            volumes = {
                **volumes,
                host_source: {
                    'bind': container_destination,
                }
            }
            setattr(namespace, self.dest, volumes)

    def __init__(self):
        self._parser = ArgumentParser()
        self._parser.add_argument('--name')
        self._parser.add_argument('--env', '-e', action='append')
        self._parser.add_argument('--publish', '-p', action=self.PublishAction)
        self._parser.add_argument('--volume', '-v', action=self.VolumeAction)
        self._parser.add_argument('--cap-drop', action='append')
        self._parser.add_argument('--cap-add', action='append')
        self._parser.add_argument('image')

    def get_arguments(self) -> Namespace:
        return self._parser.parse_args()
