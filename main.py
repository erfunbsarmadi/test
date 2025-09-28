from sheet_helper import read_sheet, write_sheet
from outlook_mailer import get_token, send_email
from gdrive_helper import download_file, cleanup_file
from gemini_helper import compose_email, suggest_subject, clarity_check
import pandas as pd

# --- Setup ---
sheet_id = "1j3TazOWluMGJZRk9TweKadKpIaE00wZ7coSyjsjcMIQ"
creds_file = "credentials.json"

df = read_sheet(sheet_id, "Sheet1!1:1000", creds_file)


token = get_token()

#prepare email
df['Email Body'][0]=compose_email(df['Professor Name'][0], df['Abstract'][0])
print(clarity_check(df['Email Body'][0]))
df['Subject'][0]=suggest_subject(df['Email Body'][0])
print(clarity_check(df['Subject'][0]))

#check email
#suggest subject
#check subject

#download_file('1zvBoRn_5hlhoiSuhptqtD6CdrgxlAryg', 'cv.pdf')





#send_email(token, recipients, subject, body, attachments = ['cv.pdf'])


write_sheet(sheet_id, 'Sheet1!A1', df, creds_file)
#cleanup_file('cv.pdf')
