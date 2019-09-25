from typing import Dict, Set, List

from capability import Capability, DEFAULT_CAPABILITIES


class CapabilitiesManager:
    CAP_ADD_CONFIG_KEY = 'CapAdd'
    CAP_DROP_CONFIG_KEY = 'CapDrop'

    def __init__(self, container_config: Dict):
        added_capabilities: List[Capability] = Capability.from_strings(container_config[self.CAP_ADD_CONFIG_KEY])
        dropped_capabilities: List[Capability] = Capability.from_strings(container_config[self.CAP_DROP_CONFIG_KEY])

        self._declared_capabilities: Set[Capability] = DEFAULT_CAPABILITIES \
            .union(added_capabilities) \
            .difference(dropped_capabilities)
        self._used_capabilities: Set[Capability] = set()

    def add_used_capability(self, capability: Capability) -> None:
        self._used_capabilities.add(capability)

    def print_report(self):
        self._print_capabilities('Container declared capabilities', self._declared_capabilities)

        self._print_capabilities('Container used capabilities', self._used_capabilities)

        over_permissioned_capabilities = self._declared_capabilities.difference(self._used_capabilities)
        self._print_capabilities('Container declared but not used capabilities (over permissioning)',
                                 over_permissioned_capabilities)

        under_permissioned_capabilities = self._used_capabilities.difference(self._declared_capabilities)
        self._print_capabilities('Container used but not declared capabilities (over permissioning)',
                                 under_permissioned_capabilities)

    @staticmethod
    def _print_capabilities(title: str, capabilities: Set[Capability]):
        print('\n', f'{title}:\n')

        sorted_capabilities = [capability.name for capability in list(capabilities)]
        sorted_capabilities.sort()

        for capability in sorted_capabilities:
            print('\t', capability)
