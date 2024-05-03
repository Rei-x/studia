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


# jakaś herezja xd
def make_generator_mem(f: Callable[[int], R]):
    @cache
    def cached_f(n):
        return f(n)

    return make_generator(cached_f)
