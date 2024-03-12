from cli.parse_stdio import parse_stdio
from log_parser import ApacheLog


def only_200(log: ApacheLog):
    return log.http_code == 200


if __name__ == "__main__":
    for log in filter(only_200, parse_stdio()):
        print(log)
