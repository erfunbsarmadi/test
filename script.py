import os
import smtplib
from email.message import EmailMessage
import uuid

def sendMail(to,subject,content):
    email_address = os.getenv("GMAIL_ADDRESS")
    email_password = os.getenv("GMAIL_APP_PASSWORD")
    print(email_address)
    print(email_password)
    
    if not email_address or not email_password:
        raise ValueError("Missing Gmail credentials. Did you set GitHub Secrets?")
    
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_address
    msg["To"] = to
    msg.set_content(content)
    
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

if __name__ == '__main__':
    sendMail("erfanbs1380@gmail.com", "Test Email", "Hello from Python + Gmail!")
    print("Email sent successfully!")
    print("Message-ID:", msgID)
