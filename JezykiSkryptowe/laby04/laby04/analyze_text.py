import subprocess
import os
import sys
import json
from typing import List, Dict
from dataclasses import dataclass


@dataclass(frozen=True)
class FileStats:
    path: str
    totalCharacters: int
    totalWords: int
    totalLines: int
    mostFrequentCharacter: str | None
    mostFrequentWord: str | None
    characterFrequency: int | None
    wordFrequency: int | None


def aggregate_stats(files_stats: List[FileStats]) -> Dict:
    """Aggregates statistics from multiple files."""
    total_characters = sum(stat.totalCharacters for stat in files_stats)
    total_words = sum(stat.totalWords for stat in files_stats)
    total_lines = sum(stat.totalLines for stat in files_stats)
    most_frequent_character = max(
        files_stats, key=lambda stat: stat.characterFrequency or 0
    ).mostFrequentCharacter
    most_frequent_word = max(
        files_stats, key=lambda stat: stat.wordFrequency or 0
    ).mostFrequentWord

    return {
        "number_of_files_read": len(files_stats),
        "total_number_of_characters": total_characters,
        "total_number_of_words": total_words,
        "total_number_of_lines": total_lines,
        "most_frequently_occurring_character": most_frequent_character or "N/A",
        "most_frequently_occurring_word": most_frequent_word or "N/A",
    }


def main(directory_path: str):
    files_stats: list[FileStats] = []

    # Start the Node.js subprocess and keep it open for sending file paths
    process = subprocess.Popen(
        ["node", "laby04/analyzeText.mjs"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )

    if process.stdout is None or process.stdin is None:
        print("Failed to open Node.js subprocess.")
        sys.exit(1)

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            print(file_path, file=process.stdin)
            process.stdin.flush()

            output = process.stdout.readline()

            file_stat = json.loads(output)
            files_stats.append(
                FileStats(
                    path=file_stat["path"],
                    totalCharacters=file_stat["totalCharacters"],
                    totalWords=file_stat["totalWords"],
                    totalLines=file_stat["totalLines"],
                    mostFrequentCharacter=file_stat.get("mostFrequentCharacter"),
                    mostFrequentWord=file_stat.get("mostFrequentWord"),
                    characterFrequency=file_stat.get("characterFrequency"),
                    wordFrequency=file_stat.get("wordFrequency"),
                )
            )

    process.stdin.close()
    process.wait()
    process.terminate()

    print(aggregate_stats(files_stats))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)
    main(sys.argv[1])
