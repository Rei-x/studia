from cli.parse_stdio import parse_stdio
from log_parser import ApacheLog


def only_night_assets(log: ApacheLog):
    return log.timestamp.hour >= 22 and log.timestamp.hour <= 6


if __name__ == "__main__":
    for log in filter(only_night_assets, parse_stdio()):
        print(log)
