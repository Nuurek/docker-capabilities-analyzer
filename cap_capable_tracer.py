from threading import Event, Thread
from typing import Dict

from bcc import BPF

from capabilities_manager import CapabilitiesManager
from capability import Capability


class CapCapableTracer:
    KERNEL_SOURCE = 'trace_cap_capable.c'
    CONTAINER_PID_MACRO = 'CONTAINER_PID'

    _thread: Thread
    _finish_event: Event

    def __init__(self, container_pid: int, config: Dict):
        self._capabilities_manager = CapabilitiesManager(config)

        with open(self.KERNEL_SOURCE, 'r') as file:
            source = file.read()
            define_macro = f'#define {self.CONTAINER_PID_MACRO} {container_pid}'
            source = define_macro + '\n' + source

        self._bpf = BPF(text=source)
        print('Started tracing')

    def start(self):
        self._bpf['events'].open_perf_buffer(self._event_callback)

        self._finish_event = Event()
        self._thread = Thread(None, self._trace_cap_capable)
        self._thread.start()

    def stop(self):
        self._finish_event.set()
        self._thread.join()
        self._capabilities_manager.print_report()

    def _trace_cap_capable(self):
        while not self._finish_event.is_set():
            self._bpf.perf_buffer_poll(timeout=1)

    def _event_callback(self, _core, data, _size):
        event = self._bpf['events'].event(data)
        capability = Capability(event.cap)
        was_granted = event.ret == 0
        print(capability, was_granted)
        self._capabilities_manager.add_used_capability(capability, was_granted)
