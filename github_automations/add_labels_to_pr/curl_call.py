import requests
from github import Github

repos_str = 'automations-angela, photo-manager'

# Replace with your GitHub access token
access_token = "Import token from env"

g = Github(access_token)
def convert_to_list(str):
    new_list= str.split(", ")
    return new_list


repos = convert_to_list(repos_str)

headers = {
    'Authorization': f'token {access_token}',
    'Accept': 'application/vnd.github+json'
}

data = {
    "name": "BOEAI",
    "color": "006b75"
        }

for repo in repos:
    url = f'https://api.github.com/repos/{repo}/labels'
    print(url)
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f' {repo} -  created successfully.')
    else:
        print(f'Failed to create label {repo}', response.text)





