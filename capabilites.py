from enum import IntEnum
from typing import List, Set


class Capabilities(IntEnum):
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
    def from_strings(cls, capabilities: List[str]) -> Set['Capabilities']:
        return set([Capabilities[capability] for capability in capabilities])


DEFAULT_CAPABILITIES = {
    Capabilities.SETPCAP,
    Capabilities.MKNOD,
    Capabilities.AUDIT_WRITE,
    Capabilities.CHOWN,
    Capabilities.NET_RAW,
    Capabilities.DAC_OVERRIDE,
    Capabilities.FOWNER,
    Capabilities.FSETID,
    Capabilities.KILL,
    Capabilities.SETGID,
    Capabilities.SETUID,
    Capabilities.NET_BIND_SERVICE,
    Capabilities.SYS_CHROOT,
    Capabilities.SETFCAP
}
