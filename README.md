# Docker Capabilities Analyzer

Docker Capabilities Analyzer is a tool for analyzing the set of capabilities configured and used by Docker container.

It uses **Docker SDK for Python** to run the container and **eBPF** (extended Berkeley Packet Filter) with interface in **bcc-python** to trace system calls.
A combination of declared capabilities and used (traced) capabilities allows to determine the set of over-permissioned capabilities.

## Installation
1. Install Python 3.7
1. Install requirements `pip install -r requirements.txt`
1. Clone BCC repository: `git clone https://github.com/iovisor/bcc.git`
1. Build BCC from source: `https://github.com/iovisor/bcc/blob/master/INSTALL.md#source`
1. Navigate to `bcc-python` source: `cd bcc/build/src/python/bcc-python`
1. Install `bcc-python` package `pip install .`

## Running
To run the tool simply start the `main.py` script using Python and pass image name, e.g.:
```
python3.7 main.py postgres
```

The script accepts some of the same options as `docker run` [command](https://docs.docker.com/engine/reference/run):

```
--name          set the name of a container
--env, -e       set an environment variable, e.g. -e "var=1"
--publish, -p   publish container port, e.g. -p "8080:80"
--volume, -v    bind volume, e.g. -v "/var/host-data:/var/container-data"
--cap-drop      drop capability, e.g. --cap-drop CHOWN
--cap-add       add capability, e.g. --cap-add NEW_RAW
--privileged    give extended privileges to a container
```
