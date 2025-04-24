import os
import asyncio
from typing import List, Optional

from okta.client import Client

def client() -> Client:
    config = {
        "orgUrl": os.getenv("OKTA_ORG_URL"),
        "authorizationMode": "SSWS",
        "token": os.getenv("OKTA_API_TOKEN"),
    }
    return Client(config)

class OktaAPI:
    """Wrapper for interacting with Okta API to fetch groups and user emails."""

    def __init__(self):
        self.client = client()

    async def does_group_exist(self, okta_group: str) -> Optional[set]:
        """Fetch an Okta group by its name."""
        groups, okta_list_metadata, err = await self.client.list_groups()
        if err:
            raise RuntimeError(f"Error fetching groups: {err}")
        for group in groups:
            if group.profile.name == okta_group:
                return group
        return None

    async def get_users_in_group(self, okta_group: object) -> List[str]:
        """Fetch email addresses of users in a group."""
        users, _, err = await self.client.list_group_users(okta_group.id)
        if err:
            raise RuntimeError(f"Error fetching users for group {okta_group.profile.name}: {err}")
        return [user.profile.email for user in users]

    async def get_emails_by_group_name(self, group_name: str) -> List[str]:
        """Convenience method to get emails by group name."""
        group = await self.does_group_exist(group_name)
        if not group:
            raise ValueError(f"Group '{group_name}' not found.")
        return await self.get_users_in_group(group)


if __name__ == "__main__":

    from dotenv import load_dotenv

    async def main():
        load_dotenv()
        okta_api = OktaAPI()
        group_name = "GitHub_Jarvis-Write"
        try:
            emails = await okta_api.get_emails_by_group_name(group_name)
            print(f"Found {len(emails)} users:")
            for email in emails:
                print(email)
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())
