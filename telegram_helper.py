import requests
import json
import os

def get_updates():
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    file = open("update_id.txt","r")
    updateID = int(file.read())
    file.close()
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={updateID}"

    response = requests.get(url)
    
    # Raise an error if something went wrong
    response.raise_for_status()
    
    # Parse JSON response
    updates = response.json()

    updateID = str(updates["result"][-1]["update_id"] + 1)
    file = open("update_id.txt","w")
    file.write(updateID)
    file.close()
    print(updateID)
    
    return updates

def send_message(text, chatID = 256684990, parse_mode = 'HTML'):
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chatID}&text={text}&parse_mode={parse_mode}"
    response = requests.get(url)
    
    # Raise an error if something went wrong
    response.raise_for_status()
    
    # Parse JSON response
    response = response.json()
    return response

if __name__ == "__main__":
    # Replace with your bot token
    text = '''<b>bold</b>, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<u>underline</u>, <ins>underline</ins>
<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
<span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>
<b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>
<a href="http://www.example.com/">inline URL</a>
<a href="tg://user?id=123456789">inline mention of a user</a>
<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
<blockquote>Block quotation started\nBlock quotation continued\nThe last line of the block quotation</blockquote>
<blockquote expandable>Expandable block quotation started\nExpandable block quotation continued\nExpandable block quotation continued\nHidden by default part of the block quotation started\nExpandable block quotation continued\nThe last line of the block quotation</blockquote>'''

    updates = get_updates()
    
    # Pretty print JSON
    print(json.dumps(updates, indent=4, ensure_ascii=False))

    updates = send_message(text)
    print(json.dumps(updates, indent=4, ensure_ascii=False))
