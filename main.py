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
if df['Last Email Sent'][i] == '':
    #clarity_check_result = 'Negative'
    #while clarity_check_result != 'Positive':
    #    lastName = df['Professor Name'][i]
    #    abstract = df['Abstract'][i]
    #    text = compose_email(lastName, abstract)
    #    clarity_check_result = clarity_check(text)
    #    print(clarity_check_result)
    #df['Email Body'][i] = text
    
    #clarity_check_result = 'Negative'
    #while clarity_check_result != 'Positive':
    #    emailBody = df['Email Body'][i]
    #    text = suggest_subject(emailBody)
    #    clarity_check_result = clarity_check(text)
    #    print(clarity_check_result)
    #df['Subject'][i] = text
    
    #token = get_token()
    #recipient = df['Email'][i]
    #subject = df['Subject'][i]
    #body = df['Email Body'][i]
 #   if send_email(token, recipient, subject, body, attachments = ['CV', 'BSc Transcripts', 'MSc Transcripts']):
    lastName = df['Professor Name'][i]
    abstract = df['Abstract'][i]
    body = compose_email(lastName, abstract)
    subject = suggest_subject(emailBody)
    text = f'''
    index = {i}\n
    Subject : {subject}\n
    Email Body :\n
    {body}'''
    send_message(text)
    
    if True:
        date = datetime.datetime.now()
        df['Last Email Sent'][i] = date.strftime("%a %d/%b/%Y")
        df['Email Body'][i] = 'First Email:\n' + df['Email Body'][i]
        
        delta = randint(7,14)
        date = date + datetime.timedelta(days=delta)

        df['Planned Reminder Date'][i] = date.strftime("%a %d/%b/%Y")

elif datetime.datetime.now().strftime("%a %d/%b/%Y") == df['Planned Reminder Date'][i] and df['Reminders Sent'][i] < 5 and df['Replied'][i] == 0:
    clarity_check_result = 'Negative'
    while clarity_check_result != 'Positive':
        emailBody = df['Email Body'][i]
        text = compose_reminder(emailBody)
        clarity_check_result = clarity_check(text)
        print(clarity_check_result)

    token = get_token()
    recipient = df['Email'][i]
    subject = 'Reminder: ' + df['Subject'][i]
    body = text
  #  if send_email(token, recipient, subject, body, attachments = ['CV', 'BSc Transcripts', 'MSc Transcripts']):
    if True:
        date = datetime.datetime.now()
        df['Last Email Sent'][i] = date.strftime("%a %d/%b/%Y")
        df['Reminders Sent'][i] = df['Reminders Sent'][i] + 1
        df['Email Body'][i] = df['Email Body'][i] + '\n\nReminder ' + str(df['Reminders Sent'][i]) + ':\n' + text
        
        while True:
            delta = randint(7,14)
            date = date + datetime.timedelta(days=delta)
            if date.weekday() < 6:
                break
            else:
                delta = -1 * delta
                date = date + datetime.timedelta(days=delta)

        df['Planned Reminder Date'][i] = date.strftime("%a %d/%b/%Y")

#check email
#suggest subject
#check subject

#download_file('1zvBoRn_5hlhoiSuhptqtD6CdrgxlAryg', 'cv.pdf')





#send_email(token, recipients, subject, body, attachments = ['cv.pdf'])


write_sheet(sheet_id, 'Sheet1!A1', df, creds_file)
#cleanup_file('cv.pdf')
