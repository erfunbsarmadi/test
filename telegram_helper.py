import requests
import json
import os

def get_updates(token, updateID):
    url = f"https://api.telegram.org/bot{token}/getUpdates?offset={updateID}"
    response = requests.get(url)
    
    # Raise an error if something went wrong
    response.raise_for_status()
    
    # Parse JSON response
    updates = response.json()
    return updates

def send_message(token, chatID, text, parse_mode = 'HTML'):
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chatID}&text={text}&parse_mode={parse_mode}"
    print(url)
    response = requests.get(url)
    
    # Raise an error if something went wrong
    #response.raise_for_status()
    
    # Parse JSON response
    updates = response.json()
    return updates

if __name__ == "__main__":
    # Replace with your bot token
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    updateID = 355402220
    chatID = 256684990
    text = 'hi'

    updates = get_updates(BOT_TOKEN, updateID)
    
    # Pretty print JSON
    print(json.dumps(updates, indent=4, ensure_ascii=False))

    updates = send_message(token, chatID, text)
    print(json.dumps(updates, indent=4, ensure_ascii=False))
