import os
import smtplib
from email.message import EmailMessage

# Get credentials from environment variables
email_address = os.getenv("ACADEMIC_EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")

# Create the email
msg = EmailMessage()
msg['Subject'] = "Test Email from Python"
msg['From'] = email_address
msg['To'] = "erfanbs1380@gmail.com"
msg.set_content("Hello, this is a test email sent from Python via Outlook!")

# Connect to Outlook SMTP server
with smtplib.SMTP('smtp.office365.com', 587) as smtp:
    smtp.starttls()  # Enable encryption
    smtp.login(email_address, email_password)
    smtp.send_message(msg)

print("Email sent successfully!")
