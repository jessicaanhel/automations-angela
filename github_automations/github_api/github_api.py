import logging
import os
import requests

from typing import List, Optional, Dict
from github_automations.github_api.github_app_token import build_github_app_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


    def get_team_id_and_org_id(self,  team_slug):
        """Only for organization accounts"""
        url = f"https://api.github.com/orgs/{self.name}/teams/{team_slug}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data["id"], data["organization"]["id"]


    def list_idp_groups_for_team(self, team_slug):
        """Only for organization accounts"""
        try:
            team_id, org_id = self.get_team_id_and_org_id(team_slug)
            url = f"https://api.github.com/organizations/{org_id}/team/{team_id}/team-sync/group-mappings"
            owner_token = os.getenv("OWNER_TOKEN")
            logger.info("Personal access token detected: " + "******" + owner_token[-10:] )
            headers_pat = {
                'Authorization': f'token {owner_token}',
                'Accept': 'application/vnd.github+json',
                'X-GitHub-Api-Version': '2022-11-28'
            }
            response = requests.get(url, headers=headers_pat)
            response.raise_for_status()
            group_details = response.json().get("groups")

            #Return the first and only one group name
            return group_details[0].get("group_name")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching IDP groups: {e}. Check App permissions")
            return []