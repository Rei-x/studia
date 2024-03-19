from collections.abc import Iterable
from cli.parse_stdio import parse_stdio
from log_parser import ApacheLog

BYTES_IN_ONE_GIGABYTE = 1024**3


def get_traffic_in_gigabytes(logs: Iterable[ApacheLog]):
    return (
        sum(log.number_of_bytes for log in logs if log.number_of_bytes is not None)
        / BYTES_IN_ONE_GIGABYTE
    )


if __name__ == "__main__":
    print(get_traffic_in_gigabytes(parse_stdio()))
