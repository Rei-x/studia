import sys

from log_parser import ApacheLog, ApacheLogTuple


def parse_stdio() -> list[ApacheLogTuple]:
    logs = []
    for line in sys.stdin:
        logs.append(ApacheLog.from_log(line).as_tuple)

    return logs
