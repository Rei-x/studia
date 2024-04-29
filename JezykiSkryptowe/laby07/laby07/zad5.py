from functools import cache
from typing import Callable, TypeVar

R = TypeVar("R")


def make_generator(f: Callable[[int], R]):
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1

    return generator


def make_generator_mem(f: Callable[[int], R]):
    saved_fun = f

    @cache
    def memoized_f(n):
        print("dict", f.__dict__)
        return saved_fun(n)

    f.__code__ = memoized_f.__call__.__code__

    return make_generator(memoized_f)
