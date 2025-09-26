import os, base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Scopes: read + send
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

def get_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("gmail", "v1", credentials=creds)

def get_message_by_id(service, message_id):
    """Retrieve a single Gmail message by its ID."""
    msg = service.users().messages().get(
        userId="me",
        id=message_id,
        format="metadata",
        metadataHeaders=["To", "Subject", "Message-ID"]
    ).execute()

    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    return {
        "id": msg["id"],
        "threadId": msg["threadId"],
        "to": headers.get("To", ""),
        "subject": headers.get("Subject", ""),
        "messageIdHeader": headers.get("Message-ID")
    }

def create_reply(to, subject, body_text, thread_id, message_id_header):
    msg = MIMEText(body_text)
    msg["to"] = to
    msg["subject"] = "Re: " + subject
    msg["In-Reply-To"] = message_id_header
    msg["References"] = message_id_header
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {"raw": raw, "threadId": thread_id}

def send_message(service, body):
    sent = service.users().messages().send(userId="me", body=body).execute()
    print("Reply sent → Gmail ID:", sent["id"], "Thread ID:", sent["threadId"])
    return sent

if __name__ == "__main__":
    service = get_service()

    # Get message ID from env or secret
    first_message_id = '199839b439a92c5b'
    if not first_message_id:
        raise ValueError("Please provide FIRST_MESSAGE_ID environment variable")

    convo = get_message_by_id(service, first_message_id)
    print("Found conversation:", convo)

    # Create and send a reply
    reply_body = "Hello again,\n\nThis is an automated reply to continue our conversation."
    reply_msg = create_reply(
        to=convo["to"],
        subject=convo["subject"],
        body_text=reply_body,
        thread_id=convo["threadId"],
        message_id_header=convo["messageIdHeader"]
    )
    send_message(service, reply_msg)
