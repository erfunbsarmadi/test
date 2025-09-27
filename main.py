from gdrive_helper import get_drive_service
from sheet_helper import read_sheet, write_sheet
from outlook_mailer import get_token, send_email
import pandas as pd

# --- Setup ---
drive_service = get_drive_service()
creds = drive_service._http.credentials  # reuse creds
sheet_id = "1j3TazOWluMGJZRk9TweKadKpIaE00wZ7coSyjsjcMIQ"

# --- Get recipients ---
df = read_sheet(sheet_id, "Sheet1!1:1000", creds)
print(df['Email'])
