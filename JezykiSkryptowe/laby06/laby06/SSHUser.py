from dataclasses import dataclass
from datetime import datetime
import re


@dataclass(frozen=True)
class SSHUser:
    username: str
    last_login: datetime | None

    def validate(self):
        return re.match(r"^[a-z_][a-z0-9_-]{0,31}$", self.username) is not None
