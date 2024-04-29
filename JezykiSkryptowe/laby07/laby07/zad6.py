import logging
from functools import wraps
from time import time
from typing import Callable, Any


def log(level: int) -> Callable:
    def decorator(func_or_class: Callable) -> Callable:
        logging.basicConfig(level=level)

        if isinstance(func_or_class, type):

            @wraps(func_or_class)
            def wrapper_class(*args, **kwargs) -> Any:
                logging.log(
                    level, f"Tworzenie instancji klasy {func_or_class.__name__}"
                )
                return func_or_class(*args, **kwargs)

            return wrapper_class
        else:

            @wraps(func_or_class)
            def wrapper(*args, **kwargs) -> Any:
                start_time = time()
                result = func_or_class(*args, **kwargs)
                duration = time() - start_time
                logging.log(
                    level,
                    f"Wywołano {func_or_class.__name__} z argumentami {args}, {kwargs}. "
                    f"Czas trwania: {duration:.4f}s, wartość zwracana: {result}",
                )
                return result

            return wrapper

    return decorator


@log(logging.DEBUG)
def example_function(x: int, y: int) -> int:
    return x + y


@log(logging.INFO)
class ExampleClass:
    def __init__(self, value: int) -> None:
        self.value = value


if __name__ == "__main__":
    example_function(1, 2)
    ExampleClass(42)
    example_function(3, 4)
    ExampleClass(1337)
    example_function(5, 6)
    ExampleClass(9001)
