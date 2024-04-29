from laby07.zad5 import make_generator_mem


def test_make_generator_mem_fibonacci():
    call_number = 0

    def fibonacci(n):
        nonlocal call_number
        call_number += 1
        if n <= 2:
            return 1
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)

    fib_generator = make_generator_mem(fibonacci)
    fib = fib_generator()

    assert next(fib) == 1
    assert next(fib) == 1
    assert next(fib) == 2
    assert next(fib) == 3
    assert next(fib) == 5
    assert next(fib) == 8

    assert call_number == 8


def test_make_generator_mem_catalan():
    def catalan(n):
        if n <= 1:
            return 1
        else:
            result = 0
            for i in range(n):
                result += catalan(i) * catalan(n - i - 1)
            return result

    catalan_generator = make_generator_mem(catalan)
    cat = catalan_generator()

    assert next(cat) == 1
    assert next(cat) == 2
    assert next(cat) == 5
    assert next(cat) == 14
    assert next(cat) == 42


def test_make_generator_mem_arithmetic_sequence():
    arithmetic_generator = make_generator_mem(lambda n: 2 * n - 1)
    seq = arithmetic_generator()

    assert next(seq) == 1
    assert next(seq) == 3
    assert next(seq) == 5
    assert next(seq) == 7
    assert next(seq) == 9
    assert next(seq) == 11


def test_make_generator_mem_geometric_sequence():
    geometric_generator = make_generator_mem(lambda n: 2 ** (n - 1))
    seq = geometric_generator()

    assert next(seq) == 1
    assert next(seq) == 2
    assert next(seq) == 4
    assert next(seq) == 8
    assert next(seq) == 16
    assert next(seq) == 32


def test_make_generator_mem_power_sequence():
    power_generator = make_generator_mem(lambda n: n**3)
    seq = power_generator()

    assert next(seq) == 1
    assert next(seq) == 8
    assert next(seq) == 27
    assert next(seq) == 64
    assert next(seq) == 125
    assert next(seq) == 216
