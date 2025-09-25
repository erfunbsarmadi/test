import os
import smtplib
from email.message import EmailMessage

email_address = os.getenv("GMAIL_ADDRESS")
email_password = os.getenv("GMAIL_APP_PASSWORD")

if not email_address or not email_password:
    raise ValueError("Missing Gmail credentials. Did you set GitHub Secrets?")

msg = EmailMessage()
msg["Subject"] = "Test Email"
msg["From"] = email_address
msg["To"] = "erfanbs1380@gmail.com"
msg.set_content("Hello from Python + Gmail!")

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login(email_address, email_password)
    smtp.send_message(msg)

print("Email sent successfully!")
