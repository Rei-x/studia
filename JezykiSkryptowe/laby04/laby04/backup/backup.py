import os
import sys
import subprocess
from datetime import datetime
from laby04.backup.utils import get_backup_dir, write_history


def create_backup(source_directory: str) -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dirname = os.path.basename(os.path.normpath(source_directory))
    backup_dir = get_backup_dir()

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    archive_name = f"{timestamp}-{dirname}.tar.gz"
    archive_path = os.path.join(backup_dir, archive_name)
    os.chdir(os.path.dirname(source_directory))
    # Creating the archive
    subprocess.run(["tar", "-czf", archive_path, dirname])

    # Writing to history
    record = {
        "date": datetime.now().isoformat(),
        "location": os.path.abspath(source_directory),
        "backup_file": archive_name,
    }
    write_history(record)

    print(f"Backup created: {archive_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python backup.py <directory-path>")
        sys.exit(1)

    source_directory: str = sys.argv[1]
    create_backup(source_directory)
