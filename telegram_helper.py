import requests
import json
import os
import pandas as pd
from outlook_mailer import get_token, send_email

def read_update_id():
    # If not present, initialize to 0
    UPDATE_FILE = "update_id.txt"
    if not os.path.exists(UPDATE_FILE):
        with open(UPDATE_FILE, "w") as f:
            f.write("0")
            f.close()
        return 0
    with open(UPDATE_FILE, "r") as f:
        s = f.read().strip()
        f.close()
        return int(s) if s.isdigit() else 0

def write_update_id(value: int):
    UPDATE_FILE = "update_id.txt"
    with open(UPDATE_FILE, "w") as f:
        f.write(str(value))
        f.close()

def get_updates(df):
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    file = open("update_id.txt","r")
    updateID = read_update_id()
    file.close()
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={updateID}"

    response = requests.get(url)
    
    # Raise an error if something went wrong
    response.raise_for_status()
    
    # Parse JSON response
    updates = response.json()

    print(json.dumps(updates, indent=4, ensure_ascii=False))
    if updates["result"]:
        write_update_id(updates["result"][-1]["update_id"] + 1)

    token = get_token()
    for update in updates["result"]:
        #try:
        if update["callback_query"]["date"] == "approve":
            text = update["callback_query"]["message"]["text"]
            parts = text.split('\n')
            
            i = parts[0]
            subject = parts[1]
            body = text[text.find(parts[2]):]
            recipient = df['Email'][i]

            #if send_email(token, recipient, subject, body, attachments = ['CV', 'BSc Transcripts', 'MSc Transcripts']):
            if True:
                df['Subject'][i] = subject
                
                if df['Last Email Sent'][i] == '':
                    df['Email Body'][i] = 'First Email:\n' + body
                else:
                    df['Reminders Sent'][i] = df['Reminders Sent'][i] + 1
                    df['Email Body'][i] = df['Email Body'][i] + '\n\nReminder ' + str(df['Reminders Sent'][i]) + ':\n' + body

                date = datetime.datetime.now()
                df['Last Email Sent'][i] = date.strftime("%a %d/%b/%Y")
                
                while True:
                    delta = randint(7,14)
                    date = date + datetime.timedelta(days=delta)
                    if date.weekday() < 6:
                        break
                    else:
                        delta = -1 * delta
                        date = date + datetime.timedelta(days=delta)
        
                df['Planned Reminder Date'][i] = date.strftime("%a %d/%b/%Y")
            
        elif update["callback_query"]["date"] == "rewrite":
            pass
        #except:
            #continue
    
    return df

def send_message(text, chatID = 256684990, parse_mode = 'HTML'):
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chatID,
        "text": text,
        "parse_mode": parse_mode,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "✅ Approve & Send", "callback_data": "approve"}],
                [{"text": "✍️ Rewrite", "callback_data": "rewrite"}]
            ]
        }
    }

    response = requests.post(url, json=payload)
    
    #url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chatID}&text={text}&reply_markup={keyboard}&parse_mode={parse_mode}"
    #response = requests.get(url)
    
    # Raise an error if something went wrong
    #response.raise_for_status()
    
    # Parse JSON response
    #response = response.json()
    return response

if __name__ == "__main__":
    # Replace with your bot token
    text = '''hi'''

    updates = send_message(text)
