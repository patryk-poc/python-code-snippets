import argparse
import os

import requests


class AzureArtifactsAPI:
    def __init__(self, organization, feed_name, personal_access_token):
        self.organization = organization
        self.feed_name = feed_name
        self.personal_access_token = personal_access_token

    def get_packages(self, package_name=None, last_n_versions=None):
        headers = {"Authorization": f"Basic {self.personal_access_token}"}
        base_url = (
            f"https://pkgs.dev.azure.com/{self.organization}/{self.feed_name}/_apis"
        )
        if package_name is None:
            package_name = "network-pg"

        url = f"{base_url}/packaging/Feeds/{self.feed_name}/Packages?$filter=startswith(normalizedName, '{package_name}')&api-version=6.0-preview.1"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(
                f"Request failed with status code {response.status_code}"
            )

        packages = response.json()["value"]
        if last_n_versions is not None:
            for package in packages:
                url = f'{base_url}/packaging/Feeds/{self.feed_name}/Packages/{package["normalizedVersion"]}/versions?$top={last_n_versions}&api-version=6.0-preview.1'
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    raise requests.exceptions.HTTPError(
                        f"Request failed with status code {response.status_code}"
                    )
                package["versions"] = response.json()["value"]
        return packages


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get information about Azure Artifacts packages"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Get information about all Azure Artifacts packages",
    )
    parser.add_argument(
        "--package", type=str, help="Specify the name of the package to retrieve"
    )
    parser.add_argument(
        "--organization",
        type=str,
        default="example",
        help="Specify the name of the Azure DevOps organization",
    )
    parser.add_argument(
        "--feed",
        type=str,
        default="automation",
        help="Specify the name of the Azure Artifacts feed",
    )
    parser.add_argument(
        "--last",
        type=int,
        help="Specify the number of latest package versions to retrieve",
    )
    args = parser.parse_args()

    organization = args.organization
    feed_name = args.feed
    personal_access_token = os.getenv("AZURE_ARTIFACTS_PAT")
    if personal_access_token is None:
        raise ValueError("Missing Azure Artifacts personal access token")

    api = AzureArtifactsAPI(organization, feed_name, personal_access_token)

    if args.all:
        packages = api.get_packages()
    else:
        package_name = args.package if args.package is not None else "network-aa"
        packages = api.get_packages(
            package_name=package_name, last_n_versions=args.last
        )

    for package in packages:
        print(package["name"], package["normalizedVersion"])
        if "versions" in package:
            for version in package["versions"]:
                print(version["normalizedVersion"])
