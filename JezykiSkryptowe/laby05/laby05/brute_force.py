from typing import List, TypedDict
from datetime import datetime, timedelta

from laby05.log_entry import LogEntry, MessageType


class AttackDetail(TypedDict):
    ip: str
    user: str | None
    count: int
    first_attempt: datetime
    last_attempt: datetime


def detect_brute_force_attacks(
    logs: List[LogEntry],
    time_threshold: int = 60,
    single_user: bool = True,
) -> List[AttackDetail]:
    attempts: dict[tuple[str, str | None], list[datetime]] = {}

    for log in logs:
        if log.type in {
            MessageType.FAILED_LOGIN,
            MessageType.INVALID_USERNAME,
            MessageType.INVALID_PASSWORD,
        }:
            ip_addresses = log.ipv4
            user = log.user if single_user else None
            timestamp = log.timestamp_with_current_year

            for ip in ip_addresses:
                key = (ip, user)
                if key not in attempts:
                    attempts[key] = []

                attempts[key] = [
                    t
                    for t in attempts[key]
                    if timestamp - t <= timedelta(seconds=time_threshold)
                ]

                attempts[key].append(timestamp)

    attacks = []
    for (ip, user), timestamps in attempts.items():
        if len(timestamps) > 3:
            attacks.append(
                {
                    "ip": ip,
                    "user": user,
                    "count": len(timestamps),
                    "first_attempt": min(timestamps),
                    "last_attempt": max(timestamps),
                }
            )

    return attacks
