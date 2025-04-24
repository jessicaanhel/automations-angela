import time
import requests
import jwt
import cryptography

# Constants
APP_ID = '331327'
INSTALLATION_ID = '37789993'
PRIVATE_KEY_PATH = 'private_keys/ops-runners.2023-06-07.private-key.pem'
GITHUB_API_VERSION = '2022-11-28'
JWT_EXPIRATION_SECONDS = 600


def load_signing_key(pem_path: str):
    """Load a private signing key from a PEM file."""
    with open(pem_path, 'rb') as pem_file:
        return pem_file.read()


def generate_jwt(app_id: str, signing_key) -> str:
    """Generate a JWT for GitHub App authentication."""
    payload = {
        'iat': int(time.time()),
        'exp': int(time.time()) + JWT_EXPIRATION_SECONDS,
        'iss': app_id
    }

    return jwt.encode(payload, signing_key, algorithm='RS256')


def get_github_access_token(jwt_token: str, installation_id: str) -> dict:
    """Request an access token for a GitHub App installation."""
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {jwt_token}",
        "X-GitHub-Api-Version": GITHUB_API_VERSION
    }

    response = requests.post(url, headers=headers)
    if response.status_code != 201:
        raise RuntimeError(f"Failed to get access token: {response.status_code} {response.text}")

    return response.json()

def build_github_app_token(app_id: str, private_key_path: str, installation_id: str) -> str:
    """
    Create a GitHub App installation token.
    :return: access token string
    """
    signing_key = load_signing_key(private_key_path)
    jwt_token = generate_jwt(app_id, signing_key)
    access_token_data = get_github_access_token(jwt_token, installation_id)
    return access_token_data['token']


def main():
    if not all([APP_ID, INSTALLATION_ID, PRIVATE_KEY_PATH]):
        print("Please set the GITHUB_APP_ID, GITHUB_INSTALLATION_ID, and GITHUB_PRIVATE_KEY_PATH environment variables.")
        return

    try:
        token = build_github_app_token(APP_ID, PRIVATE_KEY_PATH, INSTALLATION_ID)
        print(f"GitHub App token generated successfully: '{token[-5:]}...{token[:5]}'")
        print()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()