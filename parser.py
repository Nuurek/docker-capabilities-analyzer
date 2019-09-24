from argparse import ArgumentParser, Action, Namespace
from plistlib import Dict


class Parser:
    class PortAction(Action):
        def __call__(self, parser: ArgumentParser, namespace: Namespace, value: str, option_string: str = None):
            host_port, container_port = value.split(':')
            ports: Dict[str, str] = getattr(namespace, self.dest) or {}
            ports = {
                **ports,
                container_port: host_port
            }
            setattr(namespace, self.dest, ports)

    _parser = ArgumentParser()
    _parser.add_argument('--cap-drop', action='append')
    _parser.add_argument('--cap-add', action='append')
    _parser.add_argument('--env', '-e', action='append')
    _parser.add_argument('--publish', '-p', action=PortAction)
    _parser.add_argument('image')

    @classmethod
    def get_arguments(cls):
        return cls._parser.parse_args()
