#!/usr/bin/env python3
"""A simple script to generate random files."""
import argparse
import concurrent.futures
import os
import threading
from typing import List


def get_filename(number: int) -> str:
    """Get an auto generated filename."""
    if number < 1000:
        filename = f"file_{number:04}.bin"  # add leading zeros to the number
    else:
        filename = f"file_{number}.bin"
    return filename


def create_file(file_number: int, size: int) -> None:
    """Create a single file."""
    filename = get_filename(file_number)
    if os.path.exists(filename):
        print(f"File {filename} was overwritten")
    else:
        print(f"Created {filename}")

    with open(filename, "wb") as f:
        f.write(os.urandom(size))


def create_files_threads(num_files: int) -> None:
    """Create files with threads."""
    threads: List[threading.Thread] = []
    for i in range(num_files):
        thread = threading.Thread(target=create_file, args=(i + 1,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def create_files(num_files: int, size: int) -> None:
    """Create files."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(create_file, i + 1, size) for i in range(num_files)]
        for future in concurrent.futures.as_completed(futures):
            future.result()


def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(
        description="Create multiple files with a specified size"
    )
    parser.add_argument(
        "-n", "--num_files", type=int, help="number of files to create", required=True
    )
    parser.add_argument("-s", "--size", type=int, help="file size", default=1024 * 1024)

    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        exit()

    create_files(args.num_files, args.size)


if __name__ == "__main__":
    main()
