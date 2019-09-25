from queue import Queue
from threading import Thread, Event
from typing import Dict, Set, List

from capability import Capability, DEFAULT_CAPABILITIES


class CapabilitiesAnalyzer:
    CAP_ADD_CONFIG_KEY = 'CapAdd'
    CAP_DROP_CONFIG_KEY = 'CapDrop'

    _thread: Thread
    _finish_event: Event

    def __init__(self, queue: Queue, container_pid: int, container_config: Dict):
        self._queue = queue
        self._container_pid = container_pid
        self._initialize_capabilities_sets(container_config)

    def start(self):
        self._finish_event = Event()
        self._thread = Thread(None, self._consume_queue)
        self._thread.start()

    def stop(self):
        self._finish_event.set()
        self._thread.join()

    def _initialize_capabilities_sets(self, container_config: Dict) -> None:
        added_capabilities: List[Capability] = Capability.from_strings(container_config[self.CAP_ADD_CONFIG_KEY])
        dropped_capabilities: List[Capability] = Capability.from_strings(container_config[self.CAP_DROP_CONFIG_KEY])

        self._declared_capabilities: Set[Capability] = DEFAULT_CAPABILITIES \
            .union(added_capabilities) \
            .difference(dropped_capabilities)
        self._granted_capabilities: Set[Capability] = set()
        self._not_granted_capabilities: Set[Capability] = set()

    def _consume_queue(self):
        while not self._finish_event.is_set() or not self._queue.empty():
            item = self._queue.get(timeout=1)

            if item:
                if self._container_pid in item[2]:
                    self._add_used_capability(item[0], item[1])

    def _add_used_capability(self, capability: Capability, was_granted: bool) -> None:
        if was_granted:
            self._granted_capabilities.add(capability)
        else:
            self._not_granted_capabilities.add(capability)

    def print_report(self):
        self._print_capabilities('Container declared capabilities', self._declared_capabilities)

        granted_capabilities = self._granted_capabilities.intersection(self._declared_capabilities)
        self._print_capabilities('Container granted capabilities', granted_capabilities)

        over_permissioned_capabilities = self._declared_capabilities.difference(self._granted_capabilities)
        self._print_capabilities('Container declared but not granted capabilities (over permissioning)',
                                 over_permissioned_capabilities)

        self._print_capabilities('Container not granted capabilities (under permissioning)',
                                 self._not_granted_capabilities)

        print('\n')

    @staticmethod
    def _print_capabilities(title: str, capabilities: Set[Capability]):
        if len(capabilities) > 0:
            print('\n', f'{title}:\n')

            sorted_capabilities = [capability.name for capability in list(capabilities)]
            sorted_capabilities.sort()

            for capability in sorted_capabilities:
                print('\t', capability)
