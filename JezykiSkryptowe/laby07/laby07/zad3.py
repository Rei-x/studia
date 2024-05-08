from dataclasses import dataclass, field
import random
import string


@dataclass()
class PasswordGenerator:
    length: int
    count: int
    charset: list[str] = field(
        default_factory=lambda: list(string.ascii_letters + string.digits)
    )

    def __post_init__(self):
        if self.count < 0:
            raise ValueError("Count must be non-negative")
        if self.length < 0:
            raise ValueError("Length must be non-negative")
        if not self.charset:
            self.charset = ["*"]

    def __iter__(self):
        return self

    def __next__(self):
        if self.count == 0:
            raise StopIteration
        self.count -= 1
        return "".join(random.choices(self.charset, k=self.length))
