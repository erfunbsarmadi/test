from sheet_helper import read_sheet, write_sheet
from outlook_mailer import get_token, send_email
from gemini_helper import compose_email, suggest_subject, clarity_check, compose_reminder
import pandas as pd
import datetime
from random import randint
from telegram_helper import get_updates, send_message

# --- Setup ---
sheet_id = "1j3TazOWluMGJZRk9TweKadKpIaE00wZ7coSyjsjcMIQ"
creds_file = "credentials.json"

df = read_sheet(sheet_id, "Sheet1!1:1000", creds_file)
df['Reminders Sent'] = df['Reminders Sent'].astype(int)
df['Replied'] = df['Replied'].astype(int)



#prepare email
i = 0
if df['Last Email Sent'][i] == '' and datetime.datetime.now().weekday() < 6:
    lastName = df['Professor Name'][i]
    abstract = df['Abstract'][i]
    body = compose_email(lastName, abstract)
    subject = suggest_subject(emailBody)

elif datetime.datetime.now().strftime("%a %d/%b/%Y") == df['Planned Reminder Date'][i] and df['Reminders Sent'][i] < 5 and df['Replied'][i] == 0:    
    body = compose_reminder(emailBody)
    subject = 'Reminder: ' + df['Subject'][i]

text = f'''
index = {i}\n
Subject : {subject}\n
Email Body :\n
{body}'''
send_message(text)



write_sheet(sheet_id, 'Sheet1!A1', df, creds_file)
#cleanup_file('cv.pdf')
