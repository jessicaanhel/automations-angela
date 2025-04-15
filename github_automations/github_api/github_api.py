import logging
import requests
from typing import List, Optional, Dict
from github_automations.github_app_token.get_github_app_token import build_github_app_token


class GitHubAPI:
    def __init__(self, name: str, app_id: str, private_key_path: str, installation_id: str):
        self.name = name
        self.token = build_github_app_token(app_id, private_key_path, installation_id)
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json"
        }
        self.entity_type = self._detect_entity_type()

    def _detect_entity_type(self) -> str:
        """Determine if the given name is a user or an organization."""
        user_url = f"https://api.github.com/users/{self.name}"
        org_url = f"https://api.github.com/orgs/{self.name}"
        response = requests.get(user_url, headers=self.headers)
        if response.status_code == 200:
            logging.info(f"{self.name} is a GitHub user.")
            return "User"
        if response.status_code != 200:
            logging.error(f"Failed to identify GitHub user: {self.name}. Started to check if it's an org.")
            response = requests.get(org_url, headers=self.headers)
            if response.status_code == 200:
                logging.info(f"{self.name} is a GitHub organization.")
                return "Organization"
        logging.error(f"Failed to identify {self.name} as either a user or an organization.")
        logging.error(f"Status code: {response.status_code}")
        return "Unknown"

    def get_user_info(self, github_login: str) -> Dict:
        url = f"https://api.github.com/users/{github_login}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logging.error(f"Error fetching user info for '{github_login}'. Status: {response.status_code}")
            return {}
        return response.json()

    def get_repos(self) -> List[Dict]:
        """Get repositories for the given user or organization."""

        if self.entity_type == 'Unknown':
            logging.error(f"Cannot fetch repos for '{self.name}'. Entity type is unknown.")
            return []

        repos = []
        page = 1
        base_url = f"https://api.github.com/{'orgs' if self.entity_type == 'Organization' else 'users'}/{self.name}/repos"

        while True:
            url = f"{base_url}?page={page}&per_page=100"
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                logging.error(f"Error fetching repos for {self.name}. Status: {response.status_code}")
                break

            data = response.json()
            if not data:
                break
            repos.extend(data)
            page += 1
        return repos

    def get_open_pull_request(self, repo_name: str, pr_title: str) -> Optional[Dict]:
        if self.entity_type == 'Unknown':
            logging.error(f"Cannot fetch PRs for '{self.name}'. Entity type is unknown.")
            return None

        repo_full_name = f"{self.name}/{repo_name}"
        url = f"https://api.github.com/repos/{repo_full_name}/pulls?state=open"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logging.error(f"Error fetching PRs for '{repo_full_name}'. Status: {response.status_code}")
            return None

        for pr in response.json():
            if pr.get('title') == pr_title:
                return pr
        return None


    def get_default_branch(self, repo_name: str) -> Optional[str]:
        if self.entity_type == 'Unknown':
            logging.error(f"Cannot fetch repos for '{self.name}'. Entity type is unknown.")
            return []

        url = f"https://api.github.com/repos/{self.name}/{repo_name}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("default_branch")
        logging.error(f"Failed to fetch default branch for '{repo_name}'. Status: {response.status_code}")
        return None