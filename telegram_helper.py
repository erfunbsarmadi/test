import requests
import json
import os

def get_updates(token):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url)
    
    # Raise an error if something went wrong
    response.raise_for_status()
    
    # Parse JSON response
    updates = response.json()
    return updates


if __name__ == "__main__":
    # Replace with your bot token
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    updates = get_updates(BOT_TOKEN)
    
    # Pretty print JSON
    print(json.dumps(updates, indent=4, ensure_ascii=False))
