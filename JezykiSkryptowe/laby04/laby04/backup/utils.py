import os
import json
from typing import Dict


def get_backup_dir() -> str:
    return os.environ.get(
        "BACKUPS_DIR", os.path.join(os.path.expanduser("~"), ".backups")
    )


def write_history(record: Dict[str, str]) -> None:
    backup_dir = get_backup_dir()
    history_file_path = os.path.join(backup_dir, "backup_history.json")
    if not os.path.exists(history_file_path):
        with open(history_file_path, "w") as f:
            json.dump([], f)

    with open(history_file_path, "r+") as f:
        history = json.load(f)
        history.append(record)
        f.seek(0)
        json.dump(history, f)
