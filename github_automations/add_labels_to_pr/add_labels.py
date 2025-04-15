import os
import requests
from github import Github
from typing import List

# Load GitHub access token from environment variable
ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    raise EnvironmentError("❌ GitHub access token not found. Please set GITHUB_ACCESS_TOKEN in your environment.")

# Initialize GitHub client
github_client = Github(ACCESS_TOKEN)


def convert_to_list(repos_str: str) -> List[str]:
    """Converts a comma-separated string into a list of repository names."""
    return [repo.strip() for repo in repos_str.split(",") if repo.strip()]


def create_label_for_repo(repo_name: str, label_name: str, label_color: str) -> None:
    """Creates a label in the specified GitHub repository using the GitHub API."""
    url = f"https://api.github.com/repos/{repo_name}/labels"
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "name": label_name,
        "color": label_color
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"✅ Label '{label_name}' created successfully in {repo_name}.")
    elif response.status_code == 422 and "already_exists" in response.text:
        print(f"⚠️ Label '{label_name}' already exists in {repo_name}.")
    else:
        print(f"❌ Failed to create label in {repo_name}: {response.status_code}")
        print(response.text)


def main():
    repos_input = 'automations-angela, photo-manager'
    repos = convert_to_list(repos_input)
    label_name = "python"
    label_color = "006b75"

    for repo in repos:
        create_label_for_repo(repo, label_name, label_color)


if __name__ == "__main__":
    main()
