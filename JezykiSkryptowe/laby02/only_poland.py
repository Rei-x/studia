from log_parser import ApacheLog
from cli.parse_stdio import parse_stdio


def only_poland(log: ApacheLog):
    return log.host_address.endswith(".com")


if __name__ == "__main__":
    for log in filter(only_poland, parse_stdio()):
        print(log)
