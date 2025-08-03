# Imports
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from bs4 import BeautifulSoup
import base64
import email
import os.path
import string
import re

def clean_text(text):
    # Remove non-printable characters
    printable = set(string.printable)
    text = ''.join(filter(lambda x: x in printable, text))

    # Replace multiple spaces with a single space
    text = re.sub(r'[ \t]+', ' ', text)

    # Replace multiple blank lines with a single newline
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    # Strip leading/trailing whitespace
    return text.strip()

# Gmail read-only scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Auth function
def get_gmail_service():
    creds = None
    # 🔐 Try loading saved credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # 🔐 If no valid creds, prompt login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh expired token
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # 💾 Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

# 📥 Email body extractor
def get_email_body(payload):
    def extract_text(part):
        try:
            data = part['body'].get('data')
            if data:
                decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore').strip()
                if part['mimeType'] == 'text/html':
                    soup = BeautifulSoup(decoded, 'html.parser')
                    return soup.get_text(separator='\n').strip()
                return decoded
        except Exception:
            return ''
        return ''

    # Try to find plain text part first
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                return extract_text(part)
        for part in payload['parts']:
            if part['mimeType'] == 'text/html':
                return extract_text(part)
        # Nested multiparts
        for part in payload['parts']:
            if part['mimeType'].startswith('multipart'):
                return get_email_body(part)
    else:
        return extract_text(payload)

    return ''

# 📩 Read and save emails to a text file
def read_and_save_emails():
    service = get_gmail_service()
    all_emails = []
    next_page_token = None

    while True:
        response = service.users().messages().list(
           userId='me',
           maxResults=100, # Change how many emails to read
           pageToken=next_page_token,
           q='to:@gmail.com'
        ).execute()


        messages = response.get('messages', [])
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = msg_data['payload']['headers']
            subject = clean_text(next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject"))
            body = clean_text(get_email_body(msg_data['payload']))

            all_emails.append(f"Subject: {subject}\nBody:\n{body}\n{'-'*50}\n")

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    with open("emails.txt", "w", encoding="utf-8") as f:
        f.writelines(all_emails)

    print(f"✅ Saved {len(all_emails)} emails to emails.txt")

# 🏁 Run the script
read_and_save_emails()
