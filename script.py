import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Scopes for Gmail read access
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

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
            metadataHeaders=["To", "Subject"]
        ).execute()
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        to_addr = headers.get("To", "").lower()
        subj = headers.get("Subject", "").strip().lower()

        if recipient.lower() in to_addr and subject.lower() in subj:
            print(f"Found match → To: {to_addr} | Subject: {subj}")
            print("Gmail ID:", msg["id"])
            print("Thread ID:", msg["threadId"])
            return msg  # return first match

    print("No matching conversation found.")
    return None

if __name__ == "__main__":
    service = get_service()
    recipient = "erfanbs1380@gmail.com"
    subject = "githubtest subject"

    conversation = find_conversation(service, recipient, subject)
    if conversation:
        print("Conversation located successfully.")
