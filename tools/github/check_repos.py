#!/usr/bin/env python3
"""This script will check whether repositories of the user contain Github Actions or not. """

import argparse
import concurrent.futures
import os

import requests

# ANSI escape codes for text color
GREEN = "\033[32m"
RESET = "\033[0m"


class GithubActionDetector:
    GITHUB_URL = "https://api.github.com"

    def __init__(self, username):
        self.username = username
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("Please set the GITHUB_TOKEN environment variable.")
        self.headers = {"Authorization": f"token {self.token}"}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_repos(self):
        url = f"{self.GITHUB_URL}/users/{self.username}/repos"
        repos = self.session.get(url).json()
        return repos

    def check_workflow(self, repo):
        repo_name = repo["name"]
        repo_url = f"{self.GITHUB_URL}/repos/{self.username}/{repo_name}"
        repo_response = self.session.get(repo_url).json()
        default_branch = repo_response["default_branch"]
        url = f"{self.GITHUB_URL}/repos/{self.username}/{repo_name}/contents/.github/workflows?ref={default_branch}"
        response = self.session.get(url)
        if response.ok:
            print(f"{GREEN}{self.username}/{repo_name} has GitHub Actions{RESET}")
        else:
            print(f"{self.username}/{repo_name} does not have GitHub Actions")


def run_with_threads(args):
    for username in args.usernames:
        client = GithubActionDetector(username)
        user_repos = client.get_repos()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []

            for repo in user_repos:
                future = executor.submit(client.check_workflow, repo)
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as exc:
                    print(f"Error processing user: {exc}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check if GitHub user/org repositories have GitHub Actions"
    )
    parser.add_argument(
        "usernames",
        nargs="+",
        type=str,
        help="The username(s)/org name(s) on GitHub",
    )
    args = parser.parse_args()

    run_with_threads(args)
