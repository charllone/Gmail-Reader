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

