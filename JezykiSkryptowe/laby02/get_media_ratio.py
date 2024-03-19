from collections.abc import Iterable
from cli.parse_stdio import parse_stdio
from log_parser import ApacheLog


def media_ratio(logs: Iterable[ApacheLog]):
    media_requests = 0
    other_requests = 0

    for log in logs:
        if log.url and log.url.endswith((".gif", ".jpg", ".jpeg", ".xbm")):
            media_requests += 1
        else:
            other_requests += 1

    return media_requests / other_requests if other_requests > 0 else 0


if __name__ == "__main__":
    print(media_ratio(parse_stdio()))
