import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Scopes: need at least readonly
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("gmail", "v1", credentials=creds)

def search_sent_by_recipient(service, recipient, max_results=10):
    """Search sent messages to a specific recipient."""
    query = f"to:{recipient} in:sent"
    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()
    
    messages = results.get("messages", [])
    if not messages:
        print(f"No messages found to {recipient}")
        return []
    
    conversation = []
    for m in messages:
        msg = service.users().messages().get(
            userId="me",
            id=m["id"],
            format="metadata",
            metadataHeaders=["Subject", "To", "Date"]
        ).execute()
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        conversation.append({
            "id": m["id"],
            "threadId": msg["threadId"],
            "to": headers.get("To"),
            "subject": headers.get("Subject"),
            "date": headers.get("Date")
        })
    return conversation

if __name__ == "__main__":
    service = get_service()
    recipient = "erfanbs1380@gmail.com"   # 🔹 change this
    conv = search_sent_by_recipient(service, recipient)
    if conv:
        print(f"Conversation with {recipient}:")
        for m in conv:
            print(f"- [{m['date']}] To: {m['to']} | Subject: {m['subject']} | Gmail ID: {m['id']} | Thread ID: {m['threadId']}")
