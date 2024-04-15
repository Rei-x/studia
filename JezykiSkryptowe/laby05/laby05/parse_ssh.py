from pathlib import Path

from loguru import logger
from laby05.log_entry import LogEntry, MessageType


def read_log_file(file_path: Path):
    with open(file_path, "r") as file:
        for line in file:
            log = LogEntry.from_log(line)
            context_logger = logger.bind(
                timestamp=log.timestamp,
                hostname=log.hostname,
                app_component=log.app_component,
                pid=log.pid,
                event_description=log.event_description,
                original_log_line=log.original_log_line,
                size=log.byte_size,
            )
            context_logger.debug(f"Size: {log.byte_size}b")

            if (
                log.type == MessageType.SUCCESSFUL_LOGIN
                or log.type == MessageType.CONNECTION_CLOSED
            ):
                context_logger.info(
                    f"Succesful login or connection closed: {log.event_description}"
                )

            if log.type == MessageType.FAILED_LOGIN:
                context_logger.warning(f"Failed login: {log.event_description}")

            if log.type == MessageType.BREAK_IN_ATTEMPT:
                context_logger.critical(f"Break-in attempt: {log.event_description}")
            yield log
