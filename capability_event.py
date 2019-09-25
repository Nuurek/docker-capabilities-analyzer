from dataclasses import dataclass, field
from typing import List

from capability import Capability


@dataclass
class CapabilityEvent:
    capability: Capability
    was_granted: bool
    process_ids: List[int] = field(default_factory=list)
