from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def forall(pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    for el in iterable:
        if not pred(el):
            return False
    return True


def exists(pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    for el in iterable:
        if pred(el):
            return True
    return False


def atleast(n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    count = 0
    for el in iterable:
        if pred(el):
            count += 1
        if count >= n:
            return True
    return count >= n


def atmost(n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    count = 0
    for el in iterable:
        if pred(el):
            count += 1
        if count > n:
            return False
    return not count > n
