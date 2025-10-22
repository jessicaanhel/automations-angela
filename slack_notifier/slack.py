import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SlackSender:
    """Handles sending Slack messages to users."""

    def __init__(self, slack_token: str):
        self.client = WebClient(token=slack_token)

    #Add channel id or slack username
    def send_message(self, channel_id: str, message: str) -> None:
        try:
            self.client.chat_postMessage(channel=channel_id, text=message)
            logger.info(f"Message sent to {channel_id}")
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
        slack_username = f"@{self.slack_username}"
        logger.info(f"Sending message to {slack_username}")
        self.slack_sender.send_message(slack_username, message)