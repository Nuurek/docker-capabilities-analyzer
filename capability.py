from enum import IntEnum
from typing import List, Set, Union


# Capabilities taken directly from Linux kernel source
# https://github.com/torvalds/linux/blob/master/include/uapi/linux/capability.h
class Capability(IntEnum):
    CHOWN = 0
    DAC_OVERRIDE = 1
    DAC_READ_SEARCH = 2
    FOWNER = 3
    FSETID = 4
    KILL = 5
    SETGID = 6
    SETUID = 7
    SETPCAP = 8
    LINUX_IMMUTABLE = 9
    NET_BIND_SERVICE = 10
    NET_BROADCAST = 11
    NET_ADMIN = 12
    NET_RAW = 13
    IPC_LOCK = 14
    IPC_OWNER = 15
    SYS_MODULE = 16
    SYS_RAWIO = 17
    SYS_CHROOT = 18
    SYS_PTRACE = 19
    SYS_PACCT = 20
    SYS_ADMIN = 21
    SYS_BOOT = 22
    SYS_NICE = 23
    SYS_RESOURCE = 24
    SYS_TIME = 25
    SYS_TTY_CONFIG = 26
    MKNOD = 27
    LEASE = 28
    AUDIT_WRITE = 29
    AUDIT_CONTROL = 30
    SETFCAP = 31
    MAC_OVERRIDE = 32
    MAC_ADMIN = 33
    SYSLOG = 34
    WAKE_ALARM = 35
    BLOCK_SUSPEND = 36
    AUDIT_READ = 37

    @classmethod
    def from_strings(cls, capabilities: Union[List[str], None]) -> Set['Capability']:
        return set([Capability[capability] for capability in capabilities] if capabilities else [])


# Default container capabilities taken directly from Docker run reference:
# https://docs.docker.com/engine/reference/run/
DEFAULT_CAPABILITIES = {
    Capability.SETPCAP,
    Capability.MKNOD,
    Capability.AUDIT_WRITE,
    Capability.CHOWN,
    Capability.NET_RAW,
    Capability.DAC_OVERRIDE,
    Capability.FOWNER,
    Capability.FSETID,
    Capability.KILL,
    Capability.SETGID,
    Capability.SETUID,
    Capability.NET_BIND_SERVICE,
    Capability.SYS_CHROOT,
    Capability.SETFCAP
}

ALL_CAPABILITIES: Set[Capability] = set(Capability)
