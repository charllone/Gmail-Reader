# Gmail-Reader
This script will read Gmail inbox using a Gmail API in Google Cloud. It also cleans random txt and htmls to make the results clean

## HOW TO SETUP
- Go to [Google Cloud](https://console.cloud.google.com/)
- Create a new project
- Go to APIs & Services > Search for Gmail API > Click Enable
- Go to APIs & Services > Credentials
- Click “Create Credentials” > OAuth client ID
- Configure consent screen (basic app info)
- Application type: Desktop App
- Download the credentials.json file
- Go to APIs & Services > OAuth consent screen
- Add your Google account email to Test Users

## LIBRARY REQUIREMENTS

```bash
pip install --upgrade google-api-python-client

pip install --upgrade google-auth-httplib2

pip install --upgrade google-auth-oauthlib

pip install beautifulsoup4
```
## HOW IT WORKS

When you run the script, it securely connects to your Gmail account using OAuth and saves your login session so you don't have to log in again. It then connects to the Gmail API and searches your inbox for emails. For each email, the script extracts the subject and body — it prefers plain text but will convert HTML to clean text if necessary. It then cleans up the content by removing non-printable characters, extra spaces, and blank lines. Finally, the script saves all the cleaned subjects and message bodies into a single text file called emails.txt on your computer.
