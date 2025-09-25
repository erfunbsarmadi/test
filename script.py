# send_email.py
import os, json, base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_service_from_files():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, text, thread_id=None, reply_to_id=None):
    message = MIMEText(text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    if reply_to_id:
        message['In-Reply-To'] = reply_to_id
        message['References'] = reply_to_id
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}
    if thread_id:
        body['threadId'] = thread_id
    return body

def send_message(service, user_id, body):
    sent = service.users().messages().send(userId=user_id, body=body).execute()
    print("Sent: id=", sent.get('id'), "threadId=", sent.get('threadId'))
    return sent

if __name__ == "__main__":
    service = get_service_from_files()
    # Example: first email
    msg = create_message("me", "erfanbs1380@gmail.com", "Daily Update", "Hello from GitHub Actions!")
    sent = send_message(service, "me", msg)

    # Example: follow-up on same thread
    reply = create_message("me", "erfanbs1380@gmail.com", "Re: Daily Update", "This is a reminder!", thread_id = sent["threadId"])
    send_message(service, "me", reply)
