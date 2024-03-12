from collections.abc import Iterable
from cli.parse_stdio import parse_stdio
from log_parser import ApacheLog


def get_traffic_in_gigabytes(logs: Iterable[ApacheLog]):
    total_bytes = 0

    for log in logs:
        if log.number_of_bytes is not None:
            total_bytes += log.number_of_bytes

    return total_bytes / (1024**3)


if __name__ == "__main__":
    print(get_traffic_in_gigabytes(parse_stdio()))
