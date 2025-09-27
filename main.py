from gdrive_helper import get_drive_service
from sheet_helper import get_recipients, write_email_status
from outlook_mailer import get_token, send_email

# --- Setup ---
drive_service = get_drive_service()
creds = drive_service._http.credentials  # reuse creds
sheet_id = "1j3TazOWluMGJZRk9TweKadKpIaE00wZ7coSyjsjcMIQ"

# --- Get recipients ---
recipients = get_recipients(sheet_id, "Recipients!B2:B", creds)
print("📧 Recipients:", recipients)
