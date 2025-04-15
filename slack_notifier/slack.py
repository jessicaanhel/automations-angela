import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SlackSender:
    """Handles sending Slack messages to users."""

    def __init__(self, slack_token: str):
        self.client = WebClient(token=slack_token)

    def send_message(self, user: str, message: str) -> None:
        try:
            self.client.chat_postMessage(channel=user, text=message)
            logger.info(f"Message sent to {user}")
        except SlackApiError as e:
            logger.error(f"Slack API error: {e.response['error']}")
            logger.exception(e)


class SlackNotificationService:
    """Message sending via Slack."""

    def __init__(self, slack_sender: SlackSender, email: str):
        self.slack_sender = slack_sender
        self.email = email
        self.slack_username = self.email.split("@")[0]

    def notify(self, message: str) -> None:
        slack_handle = f"@{self.slack_username}"
        logger.info(f"Sending message to {slack_handle}")
        self.slack_sender.send_message(slack_handle, message)