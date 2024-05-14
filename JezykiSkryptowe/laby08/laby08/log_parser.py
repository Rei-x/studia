from dataclasses import dataclass
from datetime import datetime
from functools import cache
import re
import locale
from typing import Optional

from pydantic import BaseModel, Field


parts = [
    r"(?P<host>\S+)",  # host %h
    r"\S+",  # indent %l (unused)
    r"(?P<user>\S+)",  # user %u
    r"\[(?P<time>.+)\]",  # time %t
    r'"(?P<request>.*)"',  # request "%r"
    r"(?P<status>[0-9]+)",  # status %>s
    r"(?P<size>\S+)",  # size %b (careful, can be '-')
]
pattern = re.compile(r"\s+".join(parts) + r"\s*\Z")


@dataclass(frozen=True)
class ApacheLog(BaseModel):
    host_address: str = Field(min_length=1, max_length=255)
    timestamp: datetime
    http_method: Optional[str] = Field(
        min_length=1,
        max_length=10,
    )
    http_code: int
    url: Optional[str]
    number_of_bytes: Optional[int]
    original_log: str

    def __str__(self):
        return self.original_log

    @classmethod
    @cache
    def from_log(cls, log_line: str):
        print("called")
        match = pattern.match(log_line)

        if not match:
            raise ValueError(f"Unexpected log line: {log_line}")

        host = match.group("host")
        timestamp = match.group("time")
        request = match.group("request")
        http_method = None
        url = None

        request_info_splitted = request.split(" ")
        if len(request_info_splitted) >= 2:
            http_method, url, *_ = request_info_splitted

        http_code = match.group("status")
        number_of_bytes = match.group("size")
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

        log = cls(
            host_address=host,
            timestamp=datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z"),
            http_method=http_method,
            url=url,
            http_code=int(http_code),
            number_of_bytes=int(number_of_bytes) if number_of_bytes != "-" else None,
            original_log=log_line.strip(),
        )

        return log
