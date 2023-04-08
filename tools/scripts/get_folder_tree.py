#!/usr/bin/env python3

import argparse
import os

EXCLUDE_DIR = ["__pycache__"]


class FileTree:
    def __init__(self, path):
        self.path = path
        self.tree = {}

    def build(self):
        self._build_tree(self.path, self.tree)

    def display(self):
        self._display_tree(self.tree, 0)

    def _build_tree(self, path, tree):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path) and item not in EXCLUDE_DIR:
                tree[item] = {}
                self._build_tree(item_path, tree[item])
            elif item.endswith(".py"):
                tree[item] = None

    def _display_tree(self, tree, level):
        for key, value in tree.items():
            print("|   " * level + "|-- " + key)
            if value is not None:
                self._display_tree(value, level + 1)


def main():
    parser = argparse.ArgumentParser(
        description="Display a tree-like structure of all Python files in a given directory"
    )
    parser.add_argument(
        "-p",
        "--path",
        required=True,
        type=str,
        help="Path to directory containing Python files",
    )
    args = parser.parse_args()

    file_tree = FileTree(args.path)
    file_tree.build()
    file_tree.display()


if __name__ == "__main__":
    main()
