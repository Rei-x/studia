def acronym(list_of_strings: list[str]):
    return "".join(map(lambda s: s[0].upper() if len(s) > 0 else "", list_of_strings))


def median(numbers: list[int | float]):
    sorted_numbers = sorted(numbers)
    return (
        sorted_numbers[len(numbers) // 2]
        if len(numbers) % 2 == 1
        else (sorted_numbers[len(numbers) // 2 - 1] + sorted_numbers[len(numbers) // 2])
        / 2
    )


def sqrt_newton(x: float, epsilon: float, guess: float | None = None):
    guess = x / 2.0 if guess is None else guess

    next_guess = (guess + x / guess) / 2.0

    return (
        next_guess
        if abs(next_guess**2 - x) < epsilon
        else sqrt_newton(x, epsilon, next_guess)
    )


def make_alpha_dict(string: str):
    return {
        char: [word for word in string.split() if char in word]
        for char in sorted(set(filter(lambda x: x.isalpha(), string)))
    }


def flatten(lst):
    return [
        element
        for sublist in lst
        for element in (
            flatten(sublist) if isinstance(sublist, (list, tuple)) else [sublist]
        )
    ]
