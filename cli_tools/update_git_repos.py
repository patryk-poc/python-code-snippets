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

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s", level=logging.INFO
)


class GitRepositoryUpdater:
    """A class to perform update of all Git repositories."""

    GIT_DIR = ".git"
    PATHS_TO_EXCLUDE = (".terraform",)

    def __init__(self, path: str = ".", keywords: list = None):
        """Initialize the class.

        Args:
            path (str, optional): Root directory to start search for GIt repos. Defaults to ".".
            keywords (_type_, optional): Keywords list to be filter out some paths. Defaults to None.
        """
        self.repos = self.find_git_repos(path, keywords)

    @property
    def repositories(self):
        """All repositories path discovered."""
        return self.repos

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

    def _run_git_command(self, command: str, repo_dir: str):
        """Run a Git command in a given repository directory.

        Args:
            command (str): The Git command to run.
            repo_dir (str): The path to the repository where the command should be executed.
        """
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

    def fetch_git_remote(self, repo_dir: str):
        """Fetch remote Git repository data.

        Args:
            repo_dir (str): The path to the repository where the command should be executed.
        """
        os.chdir(repo_dir)

        self._run_git_command("git up", repo_dir)
        self._run_git_command("git fetch origin --prune", repo_dir)

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
    updater = GitRepositoryUpdater(path=parser.path, keywords=parser.keywords)
    if not updater.repositories:
        logger.warning("No Git repositories found to be synced with Git remote.")
    else:
        logger.info("Start syncing Git repositories.")
        for repo_dir in updater.repositories:
            updater.fetch_git_remote(repo_dir)


def main():
    """Main program."""
    script_dir, start_time = os.getcwd(), time.time()

    parser = CommandParser()
    # TODO implement logging to a file
    if parser.log:
        logger.info("Logging to file enabled")

    sync_git_repos(parser)

    os.chdir(script_dir)
    log_processing_time(start_time)


if __name__ == "__main__":
    main()
