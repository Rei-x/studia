from abc import ABC, abstractmethod
from datetime import datetime
from enum import StrEnum
from functools import cached_property
from ipaddress import IPv4Address
import re


class MessageType(StrEnum):
    INVALID_PASSWORD = "invalid password"
    ACCEPTED_PASSWORD = "accepted password"
    ERROR = "error"
    OTHER = "other"


class SSHLogEntry(ABC):
    timestamp: str
    hostname: str | None
    app_component: str
    pid: int
    event_description: str
    _original_log_line: str

    _user_pattern = re.compile(
        r"(invalid user |Invalid user |Failed password for invalid user |Failed password for |Accepted password for |user=)(?P<username>\w+)"
    )
    _ipv4_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    _log_pattern = re.compile(
        r"(?P<timestamp>\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s(?P<hostname>\w+)\s(?P<app_component>\w+)\[(?P<pid>\d+)\]:\s(?P<event_description>.+)"
    )

    def __init__(
        self,
        log_line: str,
    ):
        match = self._log_pattern.match(log_line)

        if match:
            self.timestamp = match.group("timestamp")
            self.hostname = match.group("hostname")
            self.app_component = match.group("app_component")
            self.pid = int(match.group("pid"))
            self.event_description = match.group("event_description")
            self._original_log_line = log_line.strip()
        else:
            raise ValueError(f"Cannot parse line: {log_line}")

    def __str__(self) -> str:
        return self._original_log_line

    def ipv4(self):
        addresses = self._ipv4_pattern.findall(self.event_description)

        if len(addresses) > 0:
            return IPv4Address(addresses[0])

        return None

    @abstractmethod
    def validate(self) -> bool:
        raise NotImplementedError

    @property
    def has_ipv4(self):
        return self.ipv4() is not None

    def __lt__(self, value: "SSHLogEntry") -> bool:
        return self.timestamp_with_current_year < value.timestamp_with_current_year

    def __gt__(self, value: "SSHLogEntry") -> bool:
        return self.timestamp_with_current_year > value.timestamp_with_current_year

    @cached_property
    @abstractmethod
    def type(self) -> MessageType:
        pass

    @cached_property
    def timestamp_with_current_year(self):
        return datetime.strptime(
            f"{datetime.now().year} {self.timestamp}", "%Y %b %d %H:%M:%S"
        )


class SSHRejectedPassword(SSHLogEntry):
    user: str

    def __init__(
        self,
        log_line: str,
    ):
        super().__init__(log_line)
        match = self._user_pattern.search(self.event_description)

        if match:
            self.user = match.group("username")
        else:
            raise ValueError(f"Cannot parse line: {log_line}")

    def validate(self) -> bool:
        match = self._log_pattern.match(self._original_log_line)
        user_match = self._user_pattern.search(self.event_description)
        if not match or not user_match:
            return False

        return (
            self.app_component == match.group("app_component")
            and str(self.pid) == match.group("pid")
            and self.event_description == match.group("event_description")
            and self.hostname == match.group("hostname")
            and self.timestamp == match.group("timestamp")
            and self.user == user_match.group("username")
        )

    @cached_property
    def type(self):
        return MessageType.INVALID_PASSWORD


class SSHAcceptedPassword(SSHLogEntry):
    user: str

    def __init__(
        self,
        log_line: str,
    ):
        super().__init__(log_line)
        match = self._user_pattern.search(self.event_description)

        if match:
            self.user = match.group("username")
        else:
            raise ValueError(f"Cannot parse line: {log_line}")

    def validate(self) -> bool:
        match = self._log_pattern.match(self._original_log_line)
        user_match = self._user_pattern.search(self.event_description)
        if not match or not user_match:
            return False

        return (
            self.app_component == match.group("app_component")
            and str(self.pid) == match.group("pid")
            and self.event_description == match.group("event_description")
            and self.hostname == match.group("hostname")
            and self.timestamp == match.group("timestamp")
            and self.user == user_match.group("username")
        )

    @cached_property
    def type(self):
        return MessageType.ACCEPTED_PASSWORD


class SSHError(SSHLogEntry):
    def validate(self) -> bool:
        match = self._log_pattern.match(self._original_log_line)

        if not match:
            return False

        return (
            self.app_component == match.group("app_component")
            and str(self.pid) == match.group("pid")
            and self.event_description == match.group("event_description")
            and self.hostname == match.group("hostname")
            and self.timestamp == match.group("timestamp")
        )

    @cached_property
    def type(self):
        return MessageType.ERROR


class OtherSSHLogEntry(SSHLogEntry):
    def validate(self) -> bool:
        match = self._log_pattern.match(self._original_log_line)

        if not match:
            return False

        return (
            self.app_component == match.group("app_component")
            and str(self.pid) == match.group("pid")
            and self.event_description == match.group("event_description")
            and self.hostname == match.group("hostname")
            and self.timestamp == match.group("timestamp")
        )

    @cached_property
    def type(self):
        return MessageType.OTHER
