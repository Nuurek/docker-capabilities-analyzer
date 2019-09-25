from queue import Queue
from threading import Event, Thread

from bcc import BPF

from capability import Capability


class CapabilitiesTracer:
    KERNEL_SOURCE = 'trace_cap_capable.c'

    _thread: Thread
    _finish_event: Event

    def __init__(self, queue: Queue):
        self._queue = queue

        self._bpf = BPF(src_file=self.KERNEL_SOURCE)
        print('Started tracing')

    def start(self):
        self._bpf['events'].open_perf_buffer(self._event_callback)

        self._finish_event = Event()
        self._thread = Thread(None, self._trace_cap_capable)
        self._thread.start()

    def stop(self):
        self._finish_event.set()
        self._thread.join()

    def _trace_cap_capable(self):
        while not self._finish_event.is_set():
            self._bpf.perf_buffer_poll(timeout=1)

    def _event_callback(self, _core, data, _size):
        event = self._bpf['events'].event(data)
        capability = Capability(event.cap)
        was_granted = event.ret == 0
        item = [capability, was_granted, list(event.tree)]
        self._queue.put(item)
