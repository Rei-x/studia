import os
import shutil
import sys
import json
import subprocess
from laby04.backup import utils
from typing import List, Dict


def list_backups() -> List[Dict[str, str]]:
    backup_dir = utils.get_backup_dir()
    history_file_path = os.path.join(backup_dir, "backup_history.json")
    with open(history_file_path, "r") as f:
        history = json.load(f)
    return history


def restore_backup(target_directory: str, backup_number: int) -> None:
    history = list_backups()
    if backup_number < 0 or backup_number >= len(history):
        print("Invalid backup number.")
        return

    backup_record = history[backup_number]
    backup_file = os.path.join(utils.get_backup_dir(), backup_record["backup_file"])

    # Clearing target directory
    for filename in os.listdir(target_directory):
        file_path = os.path.join(target_directory, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    # Extracting the archive
    subprocess.run(["tar", "-xzf", backup_file, "-C", target_directory])
    print(f"Restored {backup_file} to {target_directory}")


if __name__ == "__main__":
    target_directory: str = (
        sys.argv[1] if len(sys.argv) >= 2 else utils.get_backup_dir()
    )
    history = list_backups()
    for i, record in enumerate(reversed(history)):
        print(f"{i}: {record['date']} - {record['backup_file']}")

    backup_number: int = int(input("Enter the number of the backup to restore: "))
    restore_backup(target_directory, backup_number)
