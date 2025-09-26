import os
import json
import msal
import requests

# Config from environment
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
RECIPIENT = os.getenv("RECIPIENT_EMAIL")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]  # use cached refresh token
CACHE_FILE = "msal_cache.json"

def load_cache():
    cache = msal.SerializableTokenCache()
    if os.path.exists(CACHE_FILE):
        cache.deserialize(open(CACHE_FILE, "r").read())
    return cache

def save_cache(cache):
    if cache.has_state_changed:
        open(CACHE_FILE, "w").write(cache.serialize())

def get_token():
    cache = load_cache()
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

    accounts = app.get_accounts()
    result = None
    if accounts:
        # silent refresh with refresh token
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

    if not result:
        raise RuntimeError("No valid refresh token in msal_cache.json. Run interactive login locally first.")

    save_cache(cache)
    return result["access_token"]

def send_email(token):
    url = "https://graph.microsoft.com/v1.0/me/sendMail"
    email_msg = {
        "message": {
            "subject": "Test Email from GitHub Actions 🚀",
            "body": {
                "contentType": "HTML",
                "content": "<h3>Hello from GitHub Actions!</h3><p>This is a test email sent via Microsoft Graph API.</p>",
            },
            "toRecipients": [{"emailAddress": {"address": RECIPIENT}}],
        },
        "saveToSentItems": "true",
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=email_msg)
    if response.status_code == 202:
        print("✅ Email sent successfully!")
    else:
        print("❌ Failed:", response.status_code, response.text)

if __name__ == "__main__":
    token = get_token()
    send_email(token)
