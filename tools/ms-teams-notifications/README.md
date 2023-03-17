## Setup

Make sure you have `Python 3.10+` or newer installed with `poetry`, and then create a local `virtualenv`:

    poetry install
    poetry shell
    cd ./poc_teams_integration

Expected output should look like similar to the one below:

    Creating virtualenv poc-teams-integration in <your_local_path>
    Installing dependencies from lock file

    Package operations: 6 installs, 0 updates, 0 removals

    • Installing certifi (2022.12.7)
    • Installing charset-normalizer (3.0.1)
    • Installing idna (3.4)
    • Installing urllib3 (1.26.14)
    • Installing click (8.1.3)
    • Installing requests (2.28.2)

    Installing the current project: poc-teams-integration (0.1.0)

The local `virtualenv` with all dependencies should be installed.


## HOWTO

To run to get help:

    ./main.py --help

To send a message, first you need to setup `IncomingWebhook` in the selected MS Teams `channel`.
Then simply run:

    ./main.py -w <webhook_url>

The message will be sent to the configured channel.

## Documenation

- Create [Incoming Webhook](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)
- Create and [send messages](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#sending-a-card-using-an-incoming-webhook)
- MS Teams repository on Github with [Microsoft Teams Samples](https://github.com/OfficeDev/Microsoft-Teams-Samples)
