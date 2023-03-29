#!/usr/bin/env python3
"""A simple script to find patterns in files recursively."""
import argparse
import fnmatch
import os
from datetime import datetime


class FileSearcher:
    """A class to search for a text pattern in the file name."""

    def __init__(self, filename: str, pattern: str, root_dir: str):  # noqa
        self.filename = filename
        self.pattern = pattern
        self.root_dir = root_dir

    def search_files(self):
        """Search for a pattern in the files recursively."""
        for root, _, filenames in os.walk(self.root_dir):
            for filename in fnmatch.filter(filenames, self.filename):
                full_path = os.path.join(root, filename)
                with open(full_path) as file:
                    for line in file:
                        if self.pattern in line:
                            modified_time = datetime.fromtimestamp(
                                os.path.getmtime(full_path)
                            )
                            print(f"{full_path} last modified at {modified_time}")
                            break


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
