#!/usr/bin/env python3
"""This script will check whether repositories of the user contain Github Actions or not. Version with async."""

import argparse
import asyncio
import os

import aiohttp

# ANSI escape codes for text color
GREEN = "\033[32m"
RESET = "\033[0m"


class GithubActionDetector:
    GITHUB_URL = "https://api.github.com"

    def __init__(self, username, session):
        self.username = username
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("Please set the GITHUB_TOKEN environment variable.")
        self.headers = {"Authorization": f"token {self.token}"}
        self.session = session

    async def get_repos(self):
        url = f"{self.GITHUB_URL}/users/{self.username}/repos"
        async with self.session.get(url) as response:
            repos = await response.json()
        return repos

    async def check_workflow(self, repo):
        repo_name = repo["name"]
        repo_url = f"{self.GITHUB_URL}/repos/{self.username}/{repo_name}"
        async with self.session.get(repo_url) as repo_response:
            repo_data = await repo_response.json()
        default_branch = repo_data["default_branch"]
        url = f"{self.GITHUB_URL}/repos/{self.username}/{repo_name}/contents/.github/workflows?ref={default_branch}"
        async with self.session.get(url) as workflow_response:
            if workflow_response.ok:
                print(f"{GREEN}{self.username}/{repo_name} has GitHub Actions{RESET}")
            else:
                print(f"{self.username}/{repo_name} does not have GitHub Actions")


async def run_with_async(args):
    async with aiohttp.ClientSession(
        headers={"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    ) as session:
        tasks = []
        for username in args.usernames:
            client = GithubActionDetector(username, session)
            user_repos = await client.get_repos()

            for repo in user_repos:
                task = asyncio.create_task(client.check_workflow(repo))
                tasks.append(task)

        await asyncio.gather(*tasks)


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

    asyncio.run(run_with_async(args))
