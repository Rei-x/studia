from cli.parse_stdio import parse_stdio
from log_parser import ApacheLog


def only_friday(log: ApacheLog):
    return log.timestamp.weekday() == 4


if __name__ == "__main__":
    for log in filter(only_friday, parse_stdio()):
        print(log)
