#!/usr/bin/env python3

import os

import click
import requests


class MissingIncomingWebhook(Exception):
    pass


class MSTeamNotification:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.headers = {"Content-Type": "application/json"}

    def get_message(
        self, summary: str = "summary", title: str = "title", text: str = "test"
    ):
        message = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": summary,
            "title": title,
            "text": text,
        }
        return message

    def send_notification(self, message: dict):
        response = requests.post(self.webhook_url, json=message, headers=self.headers)
        if response.status_code == 200:
            print("Notification sent successfully")
        else:
            print(f"Failed to send notification, status code: {response.status_code}")


@click.command()
@click.option("--webhook_url", "-w", help="MS Teams incoming webhook URL.")
@click.option(
    "--summary", "-s", default="It is a summary", help="Summary of the notification."
)
@click.option(
    "--title", "-t", default="A sample title", help="Title of the notification."
)
@click.option(
    "--message", "-m", default="A sample message", help="Text of the notification."
)
def notify_ms_teams(webhook_url, summary, title, message):
    if webhook_url is None:
        try:
            webhook_url = os.environ["MS_TEAMS_INCOMING_WEBHOOK"]
        except KeyError:
            raise MissingIncomingWebhook(
                "Missing webhook. Please set env variable MS_TEAMS_INCOMING_WEBHOOK or provide it via -w flag"
            )
    click.echo(f"Sending notification.. {summary=}, {title=}, {message=}")
    notification = MSTeamNotification(webhook_url)
    message = notification.get_message(
        summary=summary,
        title=title,
        text=message,
    )
    notification.send_notification(message)


if __name__ == "__main__":
    notify_ms_teams()
