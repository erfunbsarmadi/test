from sheet_helper import read_sheet, write_sheet
from outlook_mailer import get_token, send_email
import pandas as pd

# --- Setup ---
sheet_id = "1j3TazOWluMGJZRk9TweKadKpIaE00wZ7coSyjsjcMIQ"
creds_file = "credentials.json"

# --- Get recipients ---
df = read_sheet(sheet_id, "Sheet1!1:1000", creds_file)
print(df['Email'][0])
df.loc[0, 'Email'] = 'erfanbs1380@gmail.com'
print(df['Email'][0])

write_sheet(sheet_id, 'Sheet1!A1', df, creds_file)

token = get_token()

recipients = ["erfanbs1380@gmail.com"]
subject = "Report attached"
body = "<p>Hello,<br>Here is your PDF report.</p>"

send_email(token, recipients, subject, body)
