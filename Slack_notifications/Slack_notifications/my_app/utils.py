import requests

def send_slack_notification(user_data):
    webhook_url = 'https://hooks.slack.com/services/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'  # Replace with your webhook URL
    slack_data = {
        "text": f"New User Registration:\n*Name*: {user_data['name']}\n*Email*: {user_data['email']}"
    }

    response = requests.post(
        webhook_url, json=slack_data,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is: {response.text}")
