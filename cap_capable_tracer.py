from functools import partial
from threading import Event, Thread

from bcc import BPF

from capabilites import Capabilities


class CapCapableTracer:
    KERNEL_SOURCE = 'trace_cap_capable.c'
    CONTAINER_PID_MACRO = 'CONTAINER_PID'
    # KERNEL_FUNCTION_NAME = 'trace_cap_capable'
    # SYS_CALL_NAME = 'fork'

    def __init__(self, container_pid: int, finish_event: Event):
        self._finish_event = finish_event

        with open(self.KERNEL_SOURCE, 'r') as file:
            source = file.read()
            define_macro = f'#define {self.CONTAINER_PID_MACRO} {container_pid}\n'
            source = define_macro + source
        self._bpf = BPF(text=source)
        # sys_call_name = self._bpf.get_syscall_fnname(self.SYS_CALL_NAME)
        # print(sys_call_name)
        # self._bpf.attach_kprobe(event=sys_call_name, fn_name=self.KERNEL_FUNCTION_NAME)
        self._thread: Thread = None

    def start(self):
        self._bpf['events'].open_perf_buffer(self._event_callback)

        self._thread = Thread(None, self._trace_cap_capable)
        self._thread.start()

    def stop(self):
        self._thread.join()

    def _trace_cap_capable(self):
        while not self._finish_event.is_set():
            self._bpf.perf_buffer_poll(timeout=1)

    def _event_callback(self, _core, data, _size):
        event = self._bpf["events"].event(data)
        # capability = Capabilities(event.cap)
        # print('used', capability)
        # tree = list(event.tree)
        # if event.containerPID in tree:
        #     print(event.cap, event.containerPID, tree)
        print(event.cap, event.containerPID, list(event.tree))
