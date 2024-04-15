import datetime
import random
import statistics
from typing import Iterable
from laby05.log_entry import LogEntry, MessageType


def get_random_logs_from_random_user(logs: Iterable[LogEntry]):
    user = random.choice(list(filter(lambda log: log.user is not None, logs)))

    return random.sample(
        [log for log in logs if log.user == user],
        random.randint(1, len(list(logs))),
    )


def get_average_duration_and_deviation(logs: Iterable[LogEntry]):
    session_starts: dict[int, datetime.datetime] = {}
    session_durations = []

    for log in logs:
        if "session opened" in log.event_description:
            session_starts[log.pid] = log.timestamp_with_current_year
        elif "session closed" in log.event_description and log.pid in session_starts:
            start_time = session_starts.pop(log.pid, None)
            if start_time:
                if log.timestamp_with_current_year < start_time:
                    start_time = start_time.replace(year=start_time.year - 1)

                duration = (
                    log.timestamp_with_current_year - start_time
                ).total_seconds()

                session_durations.append(duration)

    if session_durations:
        average_duration = statistics.mean(session_durations)
        std_deviation = (
            statistics.stdev(session_durations) if len(session_durations) > 2 else 0.0
        )
        return average_duration, std_deviation
    else:
        return 0.0, 0.0


def get_sessions_stats_grouped_by_user(logs: Iterable[LogEntry]):
    user_stats: dict[str, tuple[float, float]] = {}

    users = set([log.user for log in logs])

    for user in users:
        if not user:
            continue
        user_logs = [log for log in logs if log.user == user]
        user_stats[user] = get_average_duration_and_deviation(user_logs)

    return user_stats


def get_most_and_least_frequent_users(logs: Iterable[LogEntry]):
    user_logins: dict[str, int] = {}

    for log in logs:
        if log.user and log.type == MessageType.SUCCESSFUL_LOGIN:
            user_logins[log.user] = user_logins.get(log.user, 0) + 1

    most_freq_user = max(user_logins, key=lambda user: user_logins[user])
    least_freq_user = min(user_logins, key=lambda user: user_logins[user])

    return most_freq_user, least_freq_user
