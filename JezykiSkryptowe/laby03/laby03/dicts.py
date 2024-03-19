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
        "host_address": log_tuple[0],
        "timestamp": log_tuple[1],
        "http_method": log_tuple[2],
        "http_code": log_tuple[3],
        "url": log_tuple[4],
        "number_of_bytes": log_tuple[5],
    }


def log_to_dict(logs: list[ApacheLogTuple]):
    host_dictionary: dict[str, list[LogEntryDict]] = {}

    for log in logs:
        host = log[0]
        if host not in host_dictionary:
            host_dictionary[host] = []
        host_dictionary[host].append(entry_to_dict(log))

    return host_dictionary


def get_addrs(logs: dict[str, list[LogEntryDict]]):
    return list(logs.keys())


def print_dict_entry_dates(logs: dict[str, list[LogEntryDict]]):
    for host, entries in logs.items():
        first = min(entries, key=lambda x: x["timestamp"])
        last = max(entries, key=lambda x: x["timestamp"])
        successful = len([entry for entry in entries if entry["http_code"] == 200])
        total = len(entries)
        print(
            f"{host} - {total} requests - from {first['timestamp']} to {last['timestamp']} - {successful / total:.2%} successful"
        )
