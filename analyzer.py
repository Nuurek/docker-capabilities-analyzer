import docker

from compose.config.config import load, ConfigDetails, ConfigFile
from compose.cli.command import project_from_options

# read the input
# start the container
# get container's pid and declared capabilities
# trace fork -> update children pids
# trace kill -> update children pids
# trace capable -> check if in pids and add cap to set

# args = Parser.get_arguments()
config_file = ConfigFile.from_filename('docker-compose.yml')
config_details = ConfigDetails('.', [config_file])
config = load(config_details)

service_config = config[0]
print(service_config)

project = project_from_options('.', {})
print(project)

# TRACED_CONTAINER_NAME_PREFIX: str = 'traced'
# container_name: str = f'{TRACED_CONTAINER_NAME_PREFIX}_{uuid.uuid4()}'
# run_command: List[str] = ['docker', 'run', *sys.argv[1:-1], '--name', container_name, sys.argv[-1]]
#
# client: docker.DockerClient = docker.from_env()
#
# process: subprocess.Popen = subprocess.Popen(run_command)
# container = client.containers.get(container_name)
#
#
# def signal_handler(signal_number, _frame):
#     print('Signal', signal_number)
#
#
# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGINT, signal_handler)
#
# try:
#     process.wait()
# except KeyboardInterrupt:
#     print('KeyboardInterrupt')
#     process.kill()
