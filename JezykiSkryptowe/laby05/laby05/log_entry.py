from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from functools import cached_property
import re


class MessageType(StrEnum):
    SUCCESSFUL_LOGIN = "successful login"
    FAILED_LOGIN = "failed login"
    CONNECTION_CLOSED = "connection closed"
    INVALID_PASSWORD = "invalid password"
    INVALID_USERNAME = "invalid username"
    BREAK_IN_ATTEMPT = "break-in attempt"
    OTHER = "other"


@dataclass(frozen=True, kw_only=True)
class LogEntry:
    timestamp: str
    hostname: str
    app_component: str
    pid: int
    event_description: str
    original_log_line: str

    _user_pattern = re.compile(
        r"(invalid user |Invalid user |Failed password for invalid user |Failed password for |Accepted password for |user=)(?P<username>\w+)"
    )
    _ipv4_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    _log_pattern = re.compile(
        r"(?P<timestamp>\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s(?P<hostname>\w+)\s(?P<app_component>\w+)\[(?P<pid>\d+)\]:\s(?P<event_description>.+)"
    )

    @cached_property
    def type(self):
        if (
            "Accepted password" in self.event_description
            or "Accepted publickey" in self.event_description
        ):
            return MessageType.SUCCESSFUL_LOGIN
        elif (
            "Failed password" in self.event_description
            or "Failed publickey" in self.event_description
        ):
            if "invalid user" in self.event_description:
                return MessageType.INVALID_USERNAME
            elif "invalid password" in self.event_description:
                return MessageType.INVALID_PASSWORD
            else:
                return MessageType.FAILED_LOGIN

        elif "Invalid user" in self.event_description:
            return MessageType.INVALID_USERNAME
        elif "Connection closed" in self.event_description:
            return MessageType.CONNECTION_CLOSED
        elif "BREAK-IN" in self.event_description:
            return MessageType.BREAK_IN_ATTEMPT
        else:
            return MessageType.OTHER

    def __str__(self) -> str:
        return self.original_log_line.strip()

    @cached_property
    def byte_size(self):
        return len(self.original_log_line.encode("utf-8"))

    @cached_property
    def ipv4(self) -> list[str]:
        return self._ipv4_pattern.findall(self.event_description)

    @cached_property
    def user(self) -> str | None:
        match = self._user_pattern.search(self.event_description)
        return match.group("username") if match else None

    @cached_property
    def timestamp_with_current_year(self):
        return datetime.strptime(
            f"{datetime.now().year} {self.timestamp}", "%Y %b %d %H:%M:%S"
        )

    @classmethod
    def from_log(cls, log_line: str):
        match = cls._log_pattern.match(log_line)
        if match:
            return cls(
                timestamp=match.group("timestamp"),
                hostname=match.group("hostname"),
                app_component=match.group("app_component"),
                pid=int(match.group("pid")),
                event_description=match.group("event_description"),
                original_log_line=log_line.strip(),
            )
        else:
            raise ValueError(f"Cannot parse line: {log_line}")
