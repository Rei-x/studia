import datetime
from ipaddress import IPv4Address
from laby06.SSHLogEntry import (
    MessageType,
    OtherSSHLogEntry,
    SSHAcceptedPassword,
    SSHError,
    SSHLogEntry,
    SSHRejectedPassword,
)


class SSHLogJournal:
    _ssh_log_entries: list[SSHLogEntry]

    def __getitem__(self, key: int | slice | datetime.datetime | IPv4Address):
        if isinstance(key, slice):
            return self._ssh_log_entries[key.start : key.stop : key.step]
        elif isinstance(key, int):
            return self._ssh_log_entries[key]
        elif isinstance(key, datetime.datetime):
            return next(
                (
                    log
                    for log in self._ssh_log_entries
                    if log.timestamp_with_current_year == key
                ),
                None,
            )
        elif isinstance(key, IPv4Address):
            return next(
                (
                    log
                    for log in self._ssh_log_entries
                    if log.has_ipv4 and log.ipv4() == key
                ),
                None,
            )
        else:
            raise TypeError("Invalid key type")

    def __init__(self):
        self._ssh_log_entries = []

    def __len__(self):
        return len(self._ssh_log_entries)

    def __iter__(self):
        return iter(self._ssh_log_entries)

    def __contains__(self, value):
        return value in self._ssh_log_entries

    def append(self, log: str):
        if "Failed password for invalid user" in log:
            ssh_object = SSHRejectedPassword(log)
        elif "Accepted password for" in log:
            ssh_object = SSHAcceptedPassword(log)
        elif "error" in log:
            ssh_object = SSHError(log)
        else:
            ssh_object = OtherSSHLogEntry(log)

        if not ssh_object.validate():
            raise ValueError(f"Wrong data: {log}")

        self._ssh_log_entries.append(ssh_object)

    def get_logs_by_type(self, message_type: MessageType):
        return [log for log in self._ssh_log_entries if log.type == message_type]
