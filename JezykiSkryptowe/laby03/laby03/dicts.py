from datetime import datetime
from typing import TypedDict
from log_parser import ApacheLogTuple


class LogEntryDict(TypedDict):
    host_address: str
    timestamp: datetime
    http_method: str | None
    http_code: int
    url: str | None
    number_of_bytes: int | None


def entry_to_dict(log_tuple: ApacheLogTuple) -> LogEntryDict:
    return {
        "host_address": log_tuple.host_address,
        "timestamp": log_tuple.timestamp,
        "http_method": log_tuple.http_method,
        "http_code": log_tuple.http_code,
        "url": log_tuple.url,
        "number_of_bytes": log_tuple.number_of_bytes,
    }


def log_to_dict(logs: list[ApacheLogTuple]):
    host_dictionary: dict[str, list[LogEntryDict]] = {}

    for log in logs:
        host = log.host_address
        if host not in host_dictionary:
            host_dictionary[host] = []
        host_dictionary[host].append(entry_to_dict(log))

    return host_dictionary


def get_addrs(logs: dict[str, list[LogEntryDict]]):
    return [*logs]


def print_dict_entry_dates(logs: dict[str, list[LogEntryDict]]):
    for host, entries in logs.items():
        first = min(entries, key=lambda x: x["timestamp"])
        last = max(entries, key=lambda x: x["timestamp"])
        successful = len([entry for entry in entries if entry["http_code"] == 200])
        total = len(entries)
        print(
            f"{host} - {total} requests - from {first['timestamp']} to {last['timestamp']} - {successful / total:.2%} successful"
        )
