from laby07.zad1 import acronym, flatten, make_alpha_dict, median, sqrt_newton
import pytest


@pytest.mark.parametrize(
    "input_list, expected_output",
    [
        (["", "", ""], ""),
        (["Hello"], "H"),
        (["@#$", "%^&", "*()"], "@%*"),
        (["123", "456", "789"], "147"),
        (["Abc", "Def", "Ghi"], "ADG"),
        (["Hello", "Hello", "Hello"], "HHH"),
        (["This", "is", "a", "long", "string"], "TIALS"),
        ([], ""),
        (["Elo", "żelo", "123"], "EŻ1"),
    ],
)
def test_acronym(input_list, expected_output):
    assert acronym(input_list) == expected_output


@pytest.mark.parametrize(
    "input_list, expected_output",
    [
        ([1, 2, 3], 2),
        ([4, 5, 6], 5),
        ([10, 20, 30, 40, 50], 30),
        ([1.5, 2.5, 3.5], 2.5),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5.5),
        ([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], 27.5),
    ],
)
def test_median(input_list, expected_output):
    assert median(input_list) == expected_output


@pytest.mark.parametrize(
    "input_value, epsilon, expected_output",
    [
        (4, 0.0001, 2.0),
        (9, 0.000001, 3.0),
        (16, 0.000001, 4.0),
        (25, 0.000001, 5.0),
        (36, 0.000001, 6.0),
        (49, 0.000001, 7.0),
        (64, 0.000001, 8.0),
        (81, 0.000001, 9.0),
        (100, 0.000001, 10.0),
        (2, 0.000001, 1.414213562373095),
    ],
)
def test_sqrt_newton(input_value, epsilon, expected_output):
    assert pytest.approx(sqrt_newton(input_value, epsilon)) == expected_output


@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        ("", {}),
        (
            "hello",
            {
                "h": ["hello"],
                "e": ["hello"],
                "l": ["hello"],
                "o": ["hello"],
            },
        ),
        (
            "he and she",
            {
                "h": ["he", "she"],
                "e": ["he", "she"],
                "a": ["and"],
                "n": ["and"],
                "d": ["and"],
                "s": ["she"],
            },
        ),
        (
            "Hello WoRLD",
            {
                "e": ["Hello"],
                "l": ["Hello"],
                "o": ["Hello", "WoRLD"],
                "W": ["WoRLD"],
                "R": ["WoRLD"],
                "D": ["WoRLD"],
                "H": ["Hello"],
                "L": ["WoRLD"],
            },
        ),
        ("book", {"b": ["book"], "o": ["book"], "k": ["book"]}),
        (
            "hello, world!",
            {
                "h": ["hello,"],
                "e": ["hello,"],
                "l": ["hello,", "world!"],
                "o": ["hello,", "world!"],
                "w": ["world!"],
                "r": ["world!"],
                "d": ["world!"],
            },
        ),
    ],
)
def test_make_alpha_dict(input_string, expected_output):
    assert make_alpha_dict(input_string) == expected_output


@pytest.mark.parametrize(
    "nested_list, expected_output",
    [
        ([], []),
        ([1, 2, 3], [1, 2, 3]),
        ([1, [2, 3], 4], [1, 2, 3, 4]),
        ([1, [2, [3, 4], 5], 6], [1, 2, 3, 4, 5, 6]),
        ([1, (2, 3), [4, (5, 6)]], [1, 2, 3, 4, 5, 6]),
        (["a", ["b", "c"], [["d", "e"], "f"]], ["a", "b", "c", "d", "e", "f"]),
    ],
)
def test_flatten(nested_list, expected_output):
    assert flatten(nested_list) == expected_output
