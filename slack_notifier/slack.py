import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

logger = logging.getLogger(__name__)

class SlackSender:
    """Sends a  Slack message to the user"""
    def __init__(self, slack_token):
        self._slack = WebClient(token=slack_token)

    def send_message(self, user, message):
        try:
            self._slack.chat_postMessage(channel=user, text=message)
            logger.info(f"Message was sent to {user}")
        except SlackApiError as e:
            logger.error(f"Got an error: {e.response['error']}")
            logger.error(e)

class SlackUsernameMapper:
    """Maps GitHub users to Slack usernames."""
    def __init__(self, github_api):
        self.github_api = github_api

    def get_slack_login(self, github_username):
        user_data = self.github_api.get_user_info(github_username)
        if not user_data:
            return None
        slack_login = None
        if user_data.get('email'):
            slack_login = user_data['email'].replace("@*.com", "")
        elif user_data.get('name'):
            slack_login = user_data['name'].replace(" ", ".")
        return slack_login

class SlackNotificationService:
    def __init__(self, slack_notifier, username_mapper):
        self.slack_sender = slack_notifier
        self.username_mapper = username_mapper
        self.failed_output_file = "unrecognized_usernames.txt"

    def notify(self, email, message):
        """Sends a Slack message to the user."""
        slack_users = set()

        slack_username = self.username_mapper.create_slack_username(email)
        if slack_username:
            slack_users.add(f"@{slack_username}")
        else:
            logging.warning(f"No Slack username found for {email}, skipping notification.")
            self.log_unrecognized_username(email)

        for username in slack_users:
            logging.info(f"Sending message to {username}")
            self.slack_notifier.send_message(username, message)

    def log_unrecognized_users(self, email):
        """Logs unrecognized usernames into a file"""
        file_path = os.path.join(os.getcwd(), self.failed_output_file)
        with open(file_path, "a") as f:
            f.write(github_login)
        logging.info(f"User with email {github_login} doesn't exist in slack. Added to unrecognized_usernames.txt")