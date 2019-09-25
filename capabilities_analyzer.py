from queue import Queue, Empty
from threading import Thread, Event
from typing import Dict, Set, List

from capability import Capability, DEFAULT_CAPABILITIES, ALL_CAPABILITIES
from capability_event import CapabilityEvent


class CapabilitiesAnalyzer:
    CAP_ADD_CONFIG_KEY = 'CapAdd'
    CAP_DROP_CONFIG_KEY = 'CapDrop'
    PRIVILEGED_CONFIG_KEY = 'Privileged'
    ALL_CAPABILITIES_KEY = 'ALL'

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
        self._declared_capabilities: Set[Capability] = self._get_declared_capabilities(container_config)
        self._granted_capabilities: Set[Capability] = set()
        self._not_granted_capabilities: Set[Capability] = set()

    def _get_declared_capabilities(self, container_config: Dict) -> Set[Capability]:
        is_privileged = container_config[self.PRIVILEGED_CONFIG_KEY]
        if is_privileged:
            return ALL_CAPABILITIES

        added_capabilities_strings: List[str] = container_config[self.CAP_ADD_CONFIG_KEY] or []
        dropped_capabilities_strings: List[str] = container_config[self.CAP_DROP_CONFIG_KEY] or []

        if (
            self.ALL_CAPABILITIES_KEY in added_capabilities_strings and
            self.ALL_CAPABILITIES_KEY in dropped_capabilities_strings
        ):
            return set()
        elif (
            self.ALL_CAPABILITIES_KEY not in added_capabilities_strings and
            self.ALL_CAPABILITIES_KEY in dropped_capabilities_strings
        ):
            return Capability.from_strings(added_capabilities_strings)
        elif (
            self.ALL_CAPABILITIES_KEY in added_capabilities_strings and
            self.ALL_CAPABILITIES_KEY not in dropped_capabilities_strings
        ):
            dropped_capabilities = Capability.from_strings(dropped_capabilities_strings)

            return ALL_CAPABILITIES.difference(dropped_capabilities)
        else:
            added_capabilities = Capability.from_strings(added_capabilities_strings)
            dropped_capabilities = Capability.from_strings(dropped_capabilities_strings)

            return DEFAULT_CAPABILITIES \
                .union(added_capabilities) \
                .difference(dropped_capabilities)

    def _consume_queue(self):
        while not self._finish_event.is_set() or not self._queue.empty():
            try:
                event: CapabilityEvent = self._queue.get(timeout=1)

                if self._container_pid in event.process_ids:
                    self._add_used_capability(event.capability, event.was_granted)
            except Empty:
                pass

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
