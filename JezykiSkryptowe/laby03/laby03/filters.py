# c. Napisz funkcję get_entries_by_addr, która:
# i. przyjmuje jako parametr listę krotek reprezentującą log,
# ii. przyjmuje jako parametr ciąg znaków reprezentujący adres IP lub nazwę
# domenową hosta wykonującego żądanie,
# iii. waliduje podany kod statusu,
# iv. zwraca listę wpisów z danym ip.
# d. Napisz funkcję get_entries_by_code, która:
# i. przyjmuje jako parametr listę krotek reprezentującą log,
# ii. przyjmuje jako parametr kod statusu HTTP (np. 200),
# iii. waliduje podany kod statusu,
# iv. zwraca listę wpisów z danym kodem statusu.


from typing import Literal, overload
from log_parser import ApacheLogTuple


def get_entries_by_addr(logs: list[ApacheLogTuple], addr: str):
    return [log for log in logs if log.host_address == addr]


def get_entries_by_code(logs: list[ApacheLogTuple], code: int):
    return [log for log in logs if log.http_code == code]


@overload
def get_failed_reads(
    logs: list[ApacheLogTuple], combined: Literal[True]
) -> list[ApacheLogTuple]: ...


@overload
def get_failed_reads(
    logs: list[ApacheLogTuple], combined: Literal[False]
) -> tuple[list[ApacheLogTuple], list[ApacheLogTuple]]: ...


def get_failed_reads(logs: list[ApacheLogTuple], combined: bool = False):
    fourxx = []
    fivexx = []

    for log in logs:
        if 400 <= log[3] < 500:
            fourxx.append(log)
        elif 500 <= log[3] < 600:
            fivexx.append(log)

    if combined:
        return fourxx + fivexx

    return fourxx, fivexx


def get_entires_by_extension(logs: list[ApacheLogTuple], extension: str):
    return filter(lambda log: log.url is not None and log.url.endswith(extension), logs)
