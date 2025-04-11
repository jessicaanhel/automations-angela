from okta.client import Client
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()


CLIENT_ID = os.getenv("OKTA_CLIENT_ID")
SCOPES = ["okta.users.read", "okta.groups.read"]
OKTA_GROUP_NAME = "GitHub_Angry_Cockroaches_Admin"
PRIVATE_KEY_PATH = os.path.abspath("privateKey.pem")

OKTA_ORG_URL = os.getenv("OKTA_ORG_URL")
OKTA_TOKEN = os.getenv("OKTA_API_TOKEN")


config = {
    "orgUrl": OKTA_ORG_URL,
    "authorizationMode": "SSWS",
    "token": OKTA_TOKEN,
}

client = Client(config)

async def get_users():
    users, resp, err = await client.list_users()
    if err:
        print(f"Error fetching users: {err}")
    else:
        for user in users:
            print(user.profile.email)

async def get_groups():
    groups, resp, err = await client.list_groups()
    if err:
        print(f"Error fetching groups: {err}")
    else:
        for group in groups:
            print(group.profile.name)

async def main():
    await get_users()
    await get_groups()

if __name__ == "__main__":
    asyncio.run(main())