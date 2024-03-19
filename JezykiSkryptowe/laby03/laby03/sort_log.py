from log_parser import ApacheLogTuple


def sort_log(logs: list[ApacheLogTuple], by: int):
    if by not in range(6):
        raise ValueError("Invalid value for 'by'")

    return sorted(
        logs,
        key=lambda x: x[by],  # type: ignore
    )
