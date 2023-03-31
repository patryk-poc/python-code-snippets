- [Microsoft](#microsoft)
- [Scripts](#scripts)
  - [MS Teams notification](#ms-teams-notification)
  - [Documenation](#documenation)

# Microsoft

This repository might contain scripts related to MS API.
# Scripts

## MS Teams notification
To run to get help:

    ./teams_notify.py --help

To send a message, first you need to setup `IncomingWebhook` in the selected MS Teams `channel`.
Then simply run:

    ./teams_notify.py -w <webhook_url>

The message will be sent to the configured channel.

## Documenation

- Create [Incoming Webhook](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)
- Create and [send messages](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#sending-a-card-using-an-incoming-webhook)
- MS Teams repository on Github with [Microsoft Teams Samples](https://github.com/OfficeDev/Microsoft-Teams-Samples)
