from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import sys

import click
from loguru import logger

from laby05.calculate_stats import (
    get_average_duration_and_deviation,
    get_most_and_least_frequent_users,
    get_random_logs_from_random_user,
    get_sessions_stats_grouped_by_user,
)
from laby05.parse_ssh import read_log_file


class Command(Enum):
    IPV4S = "ipv4s"
    USER = "user"
    MESSAGE_TYPE = "message_type"
    GET_RANDOM_LOGS = "get_random_logs"
    STATS = "stats"
    MOST_AND_LEAST_FREQUENT_USERS = "most_and_least_frequent_users"


@dataclass
class CommandLineArgs:
    logfile: Path
    log_level: str = "INFO"
    group_by_user: bool = False


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Set the logging level",
)
@click.argument("logfile", type=click.Path(exists=True, dir_okay=False, readable=True))
@click.pass_context
def main(ctx, log_level, logfile):
    ctx.ensure_object(dict)
    ctx.obj["log_level"] = log_level
    ctx.obj["logfile"] = Path(logfile)

    logger.remove()
    logger.add(sys.stderr, level=log_level)
    logger.add("logs.log", level="DEBUG", serialize=True)


@main.command(help="Get all IPv4 addresses from the log file")
@click.pass_context
def ipv4s(ctx):
    logs = read_log_file(ctx.obj["logfile"])
    for log in logs:
        print(log.ipv4)


@main.command(help="List users from the log file")
@click.pass_context
def user(ctx):
    logs = read_log_file(ctx.obj["logfile"])
    for log in logs:
        print(log.user)


@main.command(help="List message types from the log file")
@click.pass_context
def message_type(ctx):
    logs = read_log_file(ctx.obj["logfile"])
    for log in logs:
        print(log.type)


@main.command(help="Get random logs from a random user")
@click.pass_context
def get_random_logs(ctx):
    logs = read_log_file(ctx.obj["logfile"])
    for log in get_random_logs_from_random_user(logs):
        print(log)


@main.command(help="Get the most and least frequent users")
@click.pass_context
def most_and_least_frequent_users(ctx):
    logs = read_log_file(ctx.obj["logfile"])
    users = get_most_and_least_frequent_users(logs)
    print(f"Most frequent user: {users[0]}")
    print(f"Least frequent user: {users[1]}")


@main.command(help="Get the average session duration and standard deviation")
@click.option("--group-by-user", is_flag=True, help="Group the stats by user")
@click.pass_context
def stats(ctx, group_by_user):
    logs = read_log_file(ctx.obj["logfile"])
    if group_by_user:
        stats = get_sessions_stats_grouped_by_user(logs)
        for user, (avg, dev) in stats.items():
            print(f"{user}: {avg} {dev}")
    else:
        avg, dev = get_average_duration_and_deviation(logs)
        print(f"Average: {avg} Deviation: {dev}")


if __name__ == "__main__":
    main(obj={})
