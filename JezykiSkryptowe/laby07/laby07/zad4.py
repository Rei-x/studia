from typing import Callable, TypeVar

R = TypeVar("R")


def make_generator(f: Callable[[int], R]):
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1

    return generator
