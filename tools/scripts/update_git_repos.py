#!/usr/bin/env python3
"""Simple Git repository updater.

Description: Find recursively all directories starting from the root path provided
and fetch content from the remote Git.

Requirements to run the script:
- Python 3.9+
- Git client 2.2+
- git-up extension , to be installed via `pip install git-up`
"""
import argparse
import logging
import os
import shlex
import subprocess
import time
from dataclasses import dataclass

import pkg_resources


@dataclass
class Color:
    """ANSI colors."""

    GREEN: str = "\033[32m"
    RED: str = "\033[31m"
    BLUE: str = "\033[34m"
    YELLOW: str = "\033[33m"
    RESET: str = "\033[0m"


class ColoredLogger(logging.Logger):
    """Add colors to log messages on stdout."""

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level=level)
        self._add_color_handler()

    def _add_color_handler(self):
        """Helper method to add color handler."""

        def add_handler(handler, formatter, level=None):
            handler.setFormatter(formatter)
            if level:
                handler.setLevel(level)
            self.addHandler(handler)

        formatter_info = logging.Formatter(
            f"%(asctime)s %(levelname)s {Color.GREEN}%(message)s{Color.RESET}"
        )
        formatter_error = logging.Formatter(
            f"%(asctime)s %(levelname)s {Color.RED}%(message)s{Color.RESET}"
        )

        color_handler = logging.StreamHandler()
        error_color_handler = logging.StreamHandler()

        add_handler(color_handler, formatter_info)
        add_handler(error_color_handler, formatter_error, logging.ERROR)


logging.setLoggerClass(ColoredLogger)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GitRepositoryUpdater:
    """A class to perform update of all Git repositories."""

    GIT_DIR = ".git"
    PATHS_TO_EXCLUDE = (".terraform",)
    REQUIRED_DEPENDENCY = "git-up"

    def __init__(self, path: str = ".", keywords: list = None):
        self._is_package_installed(self.REQUIRED_DEPENDENCY)
        self.repos = self.find_git_repos(path, keywords)

    def find_git_repos(self, path: str, keywords: list = None):
        """Discover all Git repositories full paths."""
        repos = []

        for root, dirs, _ in os.walk(path):
            if self.GIT_DIR in dirs:
                matching = self._is_keyword_matching(root, keywords)
                if matching:
                    repos.append(matching)
        return repos

    def _is_keyword_matching(self, root: str, keywords: list):
        """Helper method to check whether keyword is matching the repository path name."""
        repo_path = os.path.join(root, self.GIT_DIR)
        if keywords is None or any(keyword in repo_path for keyword in keywords):
            if any(path in repo_path for path in self.PATHS_TO_EXCLUDE):
                logger.warning(
                    f"Path {repo_path} is skipped as it contains reserved keyword."
                )
                return None
            return repo_path.strip(self.GIT_DIR)
        return None

    def _run_command(self, command: str, repo_dir: str):
        """Run a command inside repository."""
        logger.info(f'Running "{command}" in {repo_dir}')

        try:
            args = shlex.split(command)
            output = subprocess.check_output(
                args, shell=False, stderr=subprocess.STDOUT  # noqa: S603
            )
            if output:
                logger.info(f"Command output: {output}")
        except subprocess.CalledProcessError as e:
            logger.error(f'Error running "{command}": {e.output.decode("utf-8")}')
            return

    def _is_package_installed(self, package: str):
        package_list = {pkg.key for pkg in pkg_resources.working_set}
        if package in package_list:
            return True
        else:
            raise ValueError(
                f"Package {package} is not absent. Install via pip install"
            )

    def fetch_git_remote(self, repo_dir: str):
        """Fetch remote Git repository data."""
        logger.info(f"Entering Git directory: {repo_dir}")
        os.chdir(repo_dir)

        self._run_command("git up", repo_dir)
        self._run_command("git fetch origin --prune", repo_dir)

        logger.info(f"Finished updating {repo_dir}")


class CommandParser:
    """A class to parse input of the user from command line."""

    def __init__(self) -> None:  # noqa
        self.args = self.parse()
        self.create_properties()

    def create_properties(self) -> None:
        """Create properties based off CLI parser argument names."""
        for arg in vars(self.args):
            setattr(self, arg, getattr(self.args, arg))

    def parse(self) -> argparse.Namespace:
        """Parse input arguments from CLI."""
        parser = argparse.ArgumentParser(description="Tool to update Git repositories.")
        parser.add_argument(
            "--path",
            help="The root directory to start search for Git repositories.",
            required=True,
        )
        parser.add_argument(
            "--keywords",
            nargs="+",
            help="A list of keywords to filter repositories by.",
        )
        parser.add_argument(
            "--log", action="store_true", default=False, help="Enable logging to a file"
        )

        args = parser.parse_args()

        return args


def log_processing_time(start_time: float):
    """Log total time of execution."""
    total_time = time.time() - start_time
    hours, remainder = divmod(total_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours == 0 and minutes == 0:
        message = f"Total processing time {seconds:.2f} seconds"
    elif minutes == 0:
        message = f"Total processing time {int(hours)} hours, {int(minutes)} minutes and {seconds:.2f} seconds"
    else:
        message = (
            f"Total processing time {int(minutes)} minutes and {seconds:.2f} seconds"
        )

    logger.info(message)


def sync_git_repos(parser):
    """Sync Git remote repositories with a local copy."""
    full_path = os.path.abspath(parser.path)

    updater = GitRepositoryUpdater(path=full_path, keywords=parser.keywords)
    if not updater.repos:
        logger.warning("No Git repositories found to be synced with Git remote.")
    else:
        logger.info("Start syncing Git repositories.")
        for repo_dir in updater.repos:
            updater.fetch_git_remote(repo_dir)


def main():
    """Main program."""
    script_dir = os.getcwd()
    start_time = time.time()

    parser = CommandParser()
    if parser.log:
        logger.info("Logging to file enabled")

    sync_git_repos(parser)
    os.chdir(script_dir)
    log_processing_time(start_time)


if __name__ == "__main__":
    main()
