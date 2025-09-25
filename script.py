import os, base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Scopes: send + read to get Message-ID for threading
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly"
]

def get_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, body_text, reply_to_id=None):
    """Create MIME message and encode for Gmail API."""
    msg = MIMEText(body_text, "plain")
    msg['to'] = to
    msg['from'] = sender
    msg['subject'] = subject
    if reply_to_id:
        msg['In-Reply-To'] = reply_to_id
        msg['References'] = reply_to_id
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, body, thread_id=None):
    """Send message using Gmail API."""
    if thread_id:
        body['threadId'] = thread_id
    sent = service.users().messages().send(userId='me', body=body).execute()
    return sent

def get_message_id(service, msg_id):
    """Get the official Message-ID header of a sent message."""
    msg = service.users().messages().get(
        userId='me',
        id=msg_id,
        format='metadata',
        metadataHeaders=['Message-ID']
    ).execute()
    headers = msg['payload']['headers']
    for h in headers:
        if h['name'] == 'Message-ID':
            return h['value']
    return None

if __name__ == "__main__":
    service = get_service()
    recipient = "erfanbs1380@gmail.com"
    base_subject = "Daily Update"

    # --- Step 1: Send initial email ---
    first_body = "Hello!\n\nThis is the first message from our automation."
    first_msg = create_message("me", recipient, base_subject, first_body)
    sent_first = send_message(service, first_msg)
    print("First email sent, Gmail ID:", sent_first['id'])

    # --- Step 2: Get Message-ID for threading ---
    first_msg_id = get_message_id(service, sent_first['id'])
    print("First email Message-ID:", first_msg_id)

    # --- Step 3: Prepare follow-up email with quoted original ---
    followup_body = f"""Hello again,

This is a reminder message.

--- Previous message ---
{first_body}
"""
    reply_msg = create_message(
        "me",
        recipient,
        base_subject,           # Keep same subject to help recipient see conversation
        followup_body,
        reply_to_id=first_msg_id
    )
    sent_reply = send_message(service, reply_msg, thread_id=sent_first['threadId'])
    print("Follow-up sent, Gmail ID:", sent_reply['id'])
