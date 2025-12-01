#!/usr/bin/env python3
"""Client module for GithubOrgClient"""

from typing import List, Dict
from utils import get_json, memoize

class GithubOrgClient:
    """Github Organization Client"""

    def __init__(self, org_name: str):
        self.org_name = org_name

    def org(self) -> Dict:
        """Get org data from GitHub API"""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @memoize
    def _public_repos_url(self) -> str:
        """Return the URL to public repositories"""
        return self.org()["repos_url"]

    def public_repos(self, license_key: str = None) -> List[str]:
        """Return a list of public repo names"""
        repos = get_json(self._public_repos_url)
        repo_names = [repo["name"] for repo in repos]
        if license_key:
            repo_names = [repo["name"] for repo in repos if self.has_license(repo, license_key)]
        return repo_names

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if a repo has a specific license"""
        return repo.get("license", {}).get("key") == license_key
