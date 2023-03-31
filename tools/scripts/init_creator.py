#!/usr/bin/env python3
import argparse
import os
from pathlib import Path


class InitPyCreator:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.exclude_dirs = [".venv", "__pycache__"]

    def create_init_files(self, create_file: str = "__init__.py"):
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            dirnames[:] = [
                d for d in dirnames if d != self.root_dir and d not in self.exclude_dirs
            ]

            py_files_exist = any([f.endswith(".py") for f in filenames])

            if py_files_exist and not os.path.exists(os.path.join(dirpath, create_file)):
                Path(os.path.join(dirpath, create_file)).touch()


def main():
    parser = argparse.ArgumentParser(
        description="Recursively creates __init__.py files in a directory."
    )
    parser.add_argument(
        "-d",
        "--dir",
        required=True,
        help="The directory to start the recursive search.",
    )
    args = parser.parse_args()

    init_py_creator = InitPyCreator(args.dir)
    init_py_creator.create_init_files()


if __name__ == "__main__":
    main()
