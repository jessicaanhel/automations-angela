import os
import requests
import schedule
import time

from datetime import datetime
from dotenv import load_dotenv
from slack_notifier.slack import SlackSender

load_dotenv()

#Slack details (where you want to send the message)
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

# Notion API details (where you have your tasks)
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

slack = SlackSender(SLACK_BOT_TOKEN)

# Notion API headers
headers = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13",
}

def get_today_tasks():
    today = datetime.today().strftime('%Y-%m-%d')
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    query = {
        "filter": {
            "property": "Date",
            "date": {
                "equals": today
            }
        }
    }

    response = requests.post(url, headers=headers, json=query)
    tasks = response.json().get("results", [])

    task_list = []
    for task in tasks:
        task_name = task['properties']['Name']['title'][0]['text']['content']
        task_list.append(task_name)

    return task_list


# Function to send tasks at 9am
def send_daily_tasks():
    tasks = get_today_tasks()
    if tasks:
        task_message = "📅 *Today's Tasks:*\n"
        for i, task in enumerate(tasks, start=1):
            task_message += f"{i}. {task}\n"
        slack.send_message(CHANNEL_ID, task_message)
    else:
        slack.send_message(CHANNEL_ID, "🚫 No tasks for today.")

# Function to ask for check-in at 6pm
def send_check_in():
    check_in_message = (
        "📝 *Task Check-In:*\n"
        "How many tasks did you complete today? Please reply with a number (e.g., 3/5)."
    )
    slack.send_message(CHANNEL_ID, check_in_message)


# Schedule the tasks: 9am and 6pm
schedule.every().day.at("09:00").do(send_daily_tasks)
schedule.every().day.at("18:00").do(send_check_in)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
