import signal
import sys
from queue import Queue

from capabilities_analyzer import CapabilitiesAnalyzer
from capabilities_tracer import CapabilitiesTracer
from container_manager import ContainerManager
from parser import Parser


def main():
    parser = Parser()
    args = parser.get_arguments()

    container_manager = ContainerManager()

    events_queue = Queue()

    capabilities_tracer = CapabilitiesTracer(events_queue)
    capabilities_tracer.start()

    container_pid = container_manager.start(args)
    container_config = container_manager.get_config()

    capabilities_analyzer = CapabilitiesAnalyzer(events_queue, container_pid, container_config)
    capabilities_analyzer.start()

    def clean_up():
        container_manager.stop()
        capabilities_tracer.stop()
        capabilities_analyzer.stop()

        capabilities_analyzer.print_report()

        sys.exit()

    def signal_handler(_signal_number, _frame):
        clean_up()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    for log in container_manager.logs():
        print(log.decode())

    print('Container exited')
    clean_up()


if __name__ == '__main__':
    main()
