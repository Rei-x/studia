from dataclasses import dataclass
import os


def print_path_directories():
    path = os.getenv("PATH")
    if path is None:
        path = ""
    directories = path.split(os.pathsep)
    for directory in directories:
        if os.path.exists(directory):  # Check if directory exists
            print(directory)


def print_path_executables():
    path = os.getenv("PATH")
    if path is None:
        path = ""

    directories = path.split(os.pathsep)
    for directory in [d for d in directories if os.path.exists(d)]:
        files = os.listdir(directory)

        executables = [
            file for file in files if os.access(os.path.join(directory, file), os.X_OK)
        ]
        print(directory)
        for executable in executables:
            print(f"- {executable}")


@dataclass
class Args:
    executables: bool


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Print directories or directories and executables in PATH"
    )

    parser.add_argument(
        "-e",
        "--executables",
        action="store_true",
        help="Print directories and executables in PATH",
    )

    args = Args(**vars(parser.parse_args()))

    if args.executables:
        print_path_executables()
    else:
        print_path_directories()
