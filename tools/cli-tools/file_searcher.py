#!/usr/bin/env python3
"""A simple script to find patterns in files recursively."""
import argparse
import fnmatch
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


class FileSearcher:
    """A class to search for patterns in the file names provided."""

    def __init__(self, filename: str, pattern: str, root_dir: str):
        self.filename = filename
        self.pattern = pattern
        self.root_dir = root_dir

    def check_file_content(self, file_path: str):
        """Search for a pattern in the file."""
        with open(file_path) as file:
            for line in file:
                if self.pattern in line:
                    modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    print(f"{file_path} last modified at {modified_time}")
                    break

    def search_files(self):
        """Scan through all files starting from root dir."""
        with ThreadPoolExecutor() as executor:
            for entry in os.scandir(self.root_dir):
                if entry.is_file() and fnmatch.fnmatch(entry.name, self.filename):
                    executor.submit(self.check_file_content, entry.path)
                elif entry.is_dir():
                    subdir_searcher = FileSearcher(
                        self.filename, self.pattern, entry.path
                    )
                    subdir_searcher.search_files()


def main():
    """Program entrypoint."""
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="name of the file to search for")
    parser.add_argument("pattern", help="name of the pattern to search for")
    parser.add_argument("root_dir", help="root directory to start search from")
    args = parser.parse_args()

    searcher = FileSearcher(args.filename, args.pattern, args.root_dir)
    searcher.search_files()


if __name__ == "__main__":
    main()
