from collections.abc import Iterable
from cli.parse_stdio import parse_stdio
from log_parser import ApacheLog


def biggest_asset(logs: Iterable[ApacheLog]):
    biggest: ApacheLog | None = None

    for log in logs:
        if (
            not biggest
            or not biggest.number_of_bytes
            or (log.number_of_bytes and log.number_of_bytes > biggest.number_of_bytes)
        ):
            biggest = log

    return biggest


if __name__ == "__main__":
    biggest = biggest_asset(parse_stdio())

    print(biggest.url if biggest else "", biggest.number_of_bytes if biggest else "")
