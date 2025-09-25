import os
import smtplib
from email.message import EmailMessage

# Get credentials from environment variables
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")

# Create email
msg = EmailMessage()
msg['Subject'] = "Daily Report"
msg['From'] = email_address
msg['To'] = "erfanbs1380@gmail.com"
msg.set_content("Hello! This is a test email sent via Gmail + Python.")

# Connect to Gmail SMTP
with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()  # Upgrade to secure connection
    smtp.login(email_address, email_password)
    smtp.send_message(msg)

print("Email sent successfully!")
