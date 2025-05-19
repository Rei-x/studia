def get_time_in_seconds(time_str: str):
    hours, minutes, seconds = time_str.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)


def get_time_difference(departure: int, arrive: int):
    if departure > arrive:
        arrive += 3600 * 24
    return arrive - departure


def format_time(seconds: int):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02}"
