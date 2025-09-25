# send_email.py
import os, json, base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_service_from_files():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, text, thread_id=None):
    message = MIMEText(text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
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
    # Example: send initial email and save threadId
    sent = send_message(service, 'me', create_message('me', 'recipient@example.com', 'Test API', 'Hello from API!'))
    print("Official Gmail message id:", sent.get('id'))
    print("threadId:", sent.get('threadId'))
    # For follow ups, reuse sent['threadId'] as 'thread_id' in create_message
