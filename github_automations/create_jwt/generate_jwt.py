import time
import requests
from jwt import JWT, jwk_from_pem

# Constants
APP_ID = '331327'
INSTALLATION_ID = '37789993'
PRIVATE_KEY_PATH = 'private_keys/ops-runners.2023-06-07.private-key.pem'
GITHUB_API_VERSION = '2022-11-28'
JWT_EXPIRATION_SECONDS = 600


def load_signing_key(pem_path: str):
    """Load a private signing key from a PEM file."""
    with open(pem_path, 'rb') as pem_file:
        return jwk_from_pem(pem_file.read())


def generate_jwt(app_id: str, signing_key) -> str:
    """Generate a JWT for GitHub App authentication."""
    payload = {
        'iat': int(time.time()),
        'exp': int(time.time()) + JWT_EXPIRATION_SECONDS,
        'iss': app_id
    }

    jwt_instance = JWT()
    return jwt_instance.encode(payload, signing_key, alg='RS256')


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


def main():
    signing_key = load_signing_key(PRIVATE_KEY_PATH)
    jwt_token = generate_jwt(APP_ID, signing_key)
    print(f"✅ JWT generated successfully.\n")

    try:
        access_token_data = get_github_access_token(jwt_token, INSTALLATION_ID)
        print("✅ Access token response:")
        print(access_token_data)
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()