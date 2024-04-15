from dataclasses import dataclass
import argparse
from enum import StrEnum
from pathlib import Path
import sys

from loguru import logger


from laby05.calculate_stats import (
    get_average_duration_and_deviation,
    get_most_and_least_frequent_users,
    get_random_logs_from_random_user,
    get_sessions_stats_grouped_by_user,
)
from laby05.parse_ssh import read_log_file


class Command(StrEnum):
    IPV4S = "ipv4s"
    USER = "user"
    MESSAGE_TYPE = "message_type"
    GET_RANDOM_LOGS = "get_random_logs"
    STATS = "stats"
    MOST_AND_LEAST_FREQUENT_USERS = "most_and_least_frequent_users"


@dataclass
class CommandLineArgs:
    logfile: Path
    command: Command
    log_level: str = "INFO"
    group_by_user: bool = False


def main():
    parser = argparse.ArgumentParser(description="SSH Log Analyzer")
    parser.add_argument("logfile", help="Path to the SSH log file")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
        default="INFO",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        title="subcommands",
        required=True,
    )

    subparsers.add_parser(
        Command.IPV4S.value, help="Get all IPv4 addresses from the log file"
    )
    subparsers.add_parser(Command.USER.value, help="List users from the log file")
    subparsers.add_parser(
        Command.MESSAGE_TYPE.value, help="List message types from the log file"
    )
    subparsers.add_parser(
        Command.GET_RANDOM_LOGS.value, help="Get random logs from a random user"
    )
    stat_parser = subparsers.add_parser(
        Command.STATS.value,
        help="Get the average session duration and standard deviation",
    )
    stat_parser.add_argument(
        "--group-by-user",
        action="store_true",
        help="Group the stats by user",
        default=False,
    )
    subparsers.add_parser(
        Command.MOST_AND_LEAST_FREQUENT_USERS.value,
        help="Get the most and least frequent users",
    )

    args = parser.parse_args()

    command_line_args = CommandLineArgs(
        logfile=Path(args.logfile),
        log_level=args.log_level,
        command=args.command,
        group_by_user=getattr(args, "group_by_user", False),
    )
    logger.remove()
    logger.add(sys.stderr, level=command_line_args.log_level)
    logger.add("logs.log", level="DEBUG", serialize=True)
    logs = read_log_file(command_line_args.logfile)

    match command_line_args.command:
        case Command.IPV4S:
            for log in logs:
                print(log.ipv4)

        case Command.USER:
            for log in logs:
                print(log.user)

        case Command.MESSAGE_TYPE:
            for log in logs:
                print(log.type)

        case Command.GET_RANDOM_LOGS:
            for log in get_random_logs_from_random_user(logs):
                print(log)

        case Command.MOST_AND_LEAST_FREQUENT_USERS:
            users = get_most_and_least_frequent_users(logs)
            print(f"Most frequent user: {users[0]}")
            print(f"Least frequent user: {users[1]}")

        case Command.STATS:
            if command_line_args.group_by_user:
                stats = get_sessions_stats_grouped_by_user(logs)
                for user, (avg, dev) in stats.items():
                    print(f"{user}: {avg} {dev}")
            else:
                avg, dev = get_average_duration_and_deviation(logs)
                print(f"Average: {avg} Deviation: {dev}")


if __name__ == "__main__":
    main()
