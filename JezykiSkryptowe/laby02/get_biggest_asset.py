from collections.abc import Iterable
from cli.parse_stdio import parse_stdio
from log_parser import ApacheLog


def biggest_asset(logs: Iterable[ApacheLog]):
    return max(
        logs,
        key=lambda log: log.number_of_bytes if log.number_of_bytes else 0,
        default=None,
    )


if __name__ == "__main__":
    biggest = biggest_asset(parse_stdio())

    print(biggest.url if biggest else "", biggest.number_of_bytes if biggest else "")
