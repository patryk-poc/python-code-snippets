- [Google API](#google-api)
  - [Gmail API](#gmail-api)
- [Links](#links)

# Google API

## Gmail API

How you can create a Google API credentials file to use with the Gmail API:

Go to the Google Cloud Console.
Create a new project by clicking on the dropdown menu next to the Google Cloud Platform logo in the top left corner, and selecting "New Project".
Follow the prompts to set a project name and billing account (if required).
Once the project is created, select it from the dropdown menu in the top left corner.
Go to the "APIs & Services" dashboard by selecting it from the left-hand menu.
Click on the "Enable APIs and Services" button at the top of the page.
Search for "Gmail API" and click on the result.
Click on the "Enable" button to enable the Gmail API for your project.
Click on the "Create Credentials" button at the top of the page.
Select "OAuth client ID" as the credential type.
Choose "Desktop App" as the application type.
Enter a name for your OAuth client ID.
Click on the "Create" button to create the OAuth client ID.
Download the client secret JSON file by clicking on the "Download" button next to the client ID you just created.
Rename the downloaded file to "credentials.json".
Move the "credentials.json" file to the same directory as your Python script.

# Links

- Google [Gmail API](https://developers.google.com/gmail/api/guides)
