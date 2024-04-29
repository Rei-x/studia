from laby07.zad3 import PasswordGenerator
import pytest


def test_password_generator():
    generator = PasswordGenerator(length=8, count=5)
    passwords = list(generator)
    assert len(passwords) == 5
    for password in passwords:
        assert len(password) == 8
        assert all(char in generator.charset for char in password)


def test_password_generator_empty_charset():
    generator = PasswordGenerator(length=8, count=5, charset=[])
    passwords = list(generator)
    assert len(passwords) == 5
    for password in passwords:
        assert len(password) == 8
        assert password == "********"


def test_password_generator_custom_charset():
    charset = ["a", "b", "c"]
    generator = PasswordGenerator(length=5, count=3, charset=charset)
    passwords = list(generator)
    assert len(passwords) == 3
    for password in passwords:
        assert len(password) == 5
        assert all(char in charset for char in password)


def test_password_generator_zero_count():
    generator = PasswordGenerator(length=8, count=0)
    passwords = list(generator)
    assert len(passwords) == 0


def test_password_generator_negative_count():
    with pytest.raises(ValueError):
        generator = PasswordGenerator(length=8, count=-5)
        list(generator)
