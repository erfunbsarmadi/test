import os, base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import email

# SCOPES with send + read access
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly"
]

def get_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, text):
    msg = MIMEText(text)
    msg['to'] = to
    msg['from'] = sender
    msg['subject'] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, body):
    sent = service.users().messages().send(userId='me', body=body).execute()
    return sent

def get_message_headers(service, msg_id):
    """Fetch full email headers from Gmail API."""
    msg = service.users().messages().get(userId='me', id=msg_id, format='metadata', metadataHeaders=['Message-ID']).execute()
    headers = msg['payload']['headers']
    for h in headers:
        if h['name'] == 'Message-ID':
            return h['value']
    return None

if __name__ == "__main__":
    service = get_service()
    
    # --- Step 1: Send first email ---
    first_email = create_message("me", "erfanbs1380@gmail.com", "Daily Update", "Hello from Gmail API!")
    sent_first = send_message(service, first_email)
    print("First email sent. Gmail ID:", sent_first['id'])

    # --- Step 2: Fetch the real Message-ID from Gmail ---
    real_message_id = get_message_headers(service, sent_first['id'])
    print("Real Message-ID:", real_message_id)

    # --- Step 3: Send follow-up in same thread ---
    reply_msg = MIMEText("This is a reminder!")
    reply_msg['to'] = "erfanbs1380@gmail.com"
    reply_msg['from'] = "me"
    reply_msg['subject'] = "Re: Daily Update"
    reply_msg['In-Reply-To'] = real_message_id
    reply_msg['References'] = real_message_id

    raw_reply = base64.urlsafe_b64encode(reply_msg.as_bytes()).decode()
    reply_body = {'raw': raw_reply, 'threadId': sent_first['threadId']}

    sent_reply = send_message(service, reply_body)
    print("Reply sent in same thread. Gmail ID:", sent_reply['id'])
