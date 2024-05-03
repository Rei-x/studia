from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def forall(pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return all(pred(el) for el in iterable)


def exists(pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return any(pred(el) for el in iterable)


def atleast(n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return sum(1 for el in iterable if pred(el)) >= n


def atmost(n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return sum(1 for el in iterable if pred(el)) <= n
