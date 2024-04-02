from collections.abc import Iterable
from cli.parse_stdio import parse_stdio

from log_parser import ApacheLog


def count_status_code(status_code: int, logs: Iterable[ApacheLog]):
    return sum(1 for log in logs if log.http_code == status_code)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("status_code", type=int, help="HTTP status code to count")

    args = parser.parse_args()

    print(count_status_code(args.status_code, parse_stdio()))
