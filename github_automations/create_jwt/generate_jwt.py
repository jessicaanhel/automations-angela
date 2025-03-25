from jwt import (
    JWT,
    jwk_from_pem,
)
import time
import requests


app_id = '331327'
instalation_id = '37789993'
with open('private_keys/ops-runners.2023-06-07.private-key.pem', 'rb') as pem_file:
    signing_key = jwk_from_pem(pem_file.read())

payload = {
    # Issued at time
    'iat': int(time.time()),
    # JWT expiration time (10 minutes maximum)
    'exp': int(time.time()) + 600,
    # GitHub App's identifier
    'iss': app_id
}

# Create JWT
jwt_instance = JWT()
encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')

print(f"JWT: {encoded_jwt}")

url = f"https://api.github.com/app/installations/{instalation_id}/access_tokens"

def headers(jtw):
    return {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {jtw}",
    "X-GitHub-Api-Version": "2022-11-28"}


response = requests.post(url, headers=headers(encoded_jwt))
data = response.json()

print(data)
