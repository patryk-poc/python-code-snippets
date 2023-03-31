#!/usr/bin/env python3
"""A simple script to send notification message to MS Teams."""
import argparse
import os

import requests


class MissingIncomingWebhook(Exception):
    """Exception for missing webhook."""

    pass


class MSTeamNotification:
    """A simple MS Team notification class."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.headers = {"Content-Type": "application/json"}

    def build_message(
        self, summary: str = "summary", title: str = "title", text: str = "test"
    ):
        """Build a message object."""
        message = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": summary,
            "title": title,
            "text": text,
        }
        return message

    def send_notification(self, message: dict):
        """This function sends a notification to a webhook URL using the provided message and headers.

        Args:
            message (dict): A dictionary containing the notification message to be sent.

        Returns:
            None
        """
        response = requests.post(self.webhook_url, json=message, headers=self.headers)
        if response.status_code == 200:
            print("Notification sent successfully")
        else:
            print(f"Failed to send notification, status code: {response.status_code}")


def parse_args():
    """Parse arguments from CLI."""
    parser = argparse.ArgumentParser(description="Send Microsoft Teams notifications.")
    parser.add_argument(
        "-w",
        "--webhook",
        type=str,
        required=False,
        help="Incoming webhook URL. You can set env variable MS_TEAMS_INCOMING_WEBHOOK.",
    )
    parser.add_argument(
        "-s",
        "--summary",
        type=str,
        default="It is a summary",
        help="Summary of the notification.",
    )
    parser.add_argument(
        "-t",
        "--title",
        type=str,
        default="A sample title",
        help="Title of the notification.",
    )
    parser.add_argument(
        "-m", "--message", type=str, required=True, help="Text of the notification."
    )

    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        exit()

    return args


def notify_ms_teams():
    """Send notification to MS Teams."""
    args = parse_args()
    webhook_url = args.webhook
    summary = args.summary
    title = args.title
    message = args.message

    if webhook_url is None:
        try:
            webhook_url = os.environ["MS_TEAMS_INCOMING_WEBHOOK"]
        except KeyError:
            raise MissingIncomingWebhook(
                "Missing webhook. Please set env variable MS_TEAMS_INCOMING_WEBHOOK or provide it via -w flag"
            )

    print(f"Sending notification.. {summary=}, {title=}, {message=}")
    notification = MSTeamNotification(webhook_url)
    message = notification.build_message(
        summary=summary,
        title=title,
        text=message,
    )
    notification.send_notification(message)


if __name__ == "__main__":
    notify_ms_teams()
