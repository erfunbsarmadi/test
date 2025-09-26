import base64
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

def find_conversation(service, recipient, subject, max_results=50):
    """Find a conversation in Sent folder by recipient and subject."""
    results = service.users().messages().list(
        userId="me",
        labelIds=["SENT"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    for m in messages:
        msg = service.users().messages().get(
            userId="me",
            id=m["id"],
            format="metadata",
            metadataHeaders=["To", "Subject", "Message-ID"]
        ).execute()
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        to_addr = headers.get("To", "").lower()
        subj = headers.get("Subject", "").strip().lower()
        msg_id_header = headers.get("Message-ID")

        if recipient.lower() in to_addr and subject.lower() in subj:
            print(f"Found match → To: {to_addr} | Subject: {subj}")
            return {
                "id": msg["id"],
                "threadId": msg["threadId"],
                "to": to_addr,
                "subject": subj,
                "messageIdHeader": msg_id_header
            }

    print("No matching conversation found.")
    return None

def create_reply(to, subject, body_text, thread_id, message_id_header):
    """Create a reply message with proper threading headers."""
    msg = MIMEText(body_text)
    msg["to"] = to
    msg["subject"] = "Re: " + subject
    msg["In-Reply-To"] = message_id_header
    msg["References"] = message_id_header
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {"raw": raw, "threadId": thread_id}

def send_message(service, body):
    """Send message using Gmail API."""
    sent = service.users().messages().send(userId="me", body=body).execute()
    print("Reply sent → Gmail ID:", sent["id"], "Thread ID:", sent["threadId"])
    return sent

if __name__ == "__main__":
    service = get_service()
    recipient = "erfanbs1380@gmail.com"
    subject = "githubtest subject"

    # Step 1: Locate the conversation
    convo = find_conversation(service, recipient, subject)

    if convo:
        # Step 2: Create a reply
        reply_body = "Hello again,\n\nThis is an automated reply to continue our conversation."
        reply_msg = create_reply(
            to=convo["to"],
            subject=convo["subject"],
            body_text=reply_body,
            thread_id=convo["threadId"],
            message_id_header=convo["messageIdHeader"]
        )

        # Step 3: Send reply
        send_message(service, reply_msg)
