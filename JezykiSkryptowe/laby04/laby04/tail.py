from collections import deque
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import sys
import argparse
from dataclasses import dataclass
from typing import Optional


@dataclass
class TailArgs:
    file: Optional[str]
    lines: int = 10
    follow: bool = False


def tail(file_path: str, lines: int = 10) -> None:
    try:
        with open(file_path, "r") as file:
            for line in deque(file, lines):
                print(line, end="")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        sys.exit(1)


class TailFollower(FileSystemEventHandler):
    def __init__(self, file_path: str, lines: int) -> None:
        self.file_path = file_path
        self.lines = lines

    def on_modified(self, event) -> None:
        if event.src_path == self.file_path:
            tail(self.file_path, self.lines)


def follow(file_path: str, lines: int) -> None:
    event_handler = TailFollower(file_path, lines)
    observer = Observer()
    observer.schedule(event_handler, path=file_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def parse_args() -> TailArgs:
    parser = argparse.ArgumentParser(description="Python Tail")
    parser.add_argument("file", nargs="?", help="File path to read from.")
    parser.add_argument(
        "--lines", type=int, default=10, help="Number of lines to read from the end."
    )
    parser.add_argument(
        "--follow", action="store_true", help="Follow the file changes."
    )
    args = parser.parse_args()
    return TailArgs(file=args.file, lines=args.lines, follow=args.follow)


def main() -> None:
    args = parse_args()

    if args.follow and args.file:
        follow(args.file, args.lines)
    elif args.file:
        tail(args.file, args.lines)
    elif not args.file and args.follow:
        print("Cannot follow stdin.", file=sys.stderr)
    else:
        for line in deque(sys.stdin, args.lines):
            print(line, end="")


if __name__ == "__main__":
    main()
