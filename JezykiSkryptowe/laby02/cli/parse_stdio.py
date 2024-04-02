from log_parser import ApacheLog
import sys


# slow one
# def parse_stdio():
#     logs = []
#     for line in sys.stdin:
#         logs.append(ApacheLog.from_log(line))

#     return logs


def parse_stdio():
    for line in sys.stdin:
        yield ApacheLog.from_log(line)
