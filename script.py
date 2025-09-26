import os
import base64
import requests
import msal

# --- Config ---
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]
CACHE_FILE = "msal_cache.json"


# ------------------------
# Auth / Token Management
# ------------------------
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
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
    if not result:
        raise RuntimeError("No valid refresh token in msal_cache.json. Run interactive login locally first.")
    save_cache(cache)
    return result["access_token"]


# ------------------------
# OneDrive Helper
# ------------------------
def download_onedrive_file(token, file_path):
    """
    file_path → relative path inside OneDrive (e.g. 'Documents/report.pdf')
    Returns (filename, base64_bytes)
    """
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{file_path}:/content"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"❌ Failed to fetch {file_path} from OneDrive: {resp.status_code} {resp.text}")

    filename = os.path.basename(file_path)
    encoded = base64.b64encode(resp.content).decode("utf-8")
    return filename, encoded


# ------------------------
# Send Email
# ------------------------
def send_email(token, recipient, subject, body_html, onedrive_files=None):
    """
    Send an email via Microsoft Graph.
    - recipient: email address
    - subject: string
    - body_html: string (HTML)
    - onedrive_files: list of file paths in OneDrive
    """
    attachments = []
    if onedrive_files:
        for path in onedrive_files:
            filename, encoded = download_onedrive_file(token, path)
            attachments.append({
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": filename,
                "contentType": "application/pdf",
                "contentBytes": encoded,
            })

    email_msg = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": body_html},
            "toRecipients": [{"emailAddress": {"address": recipient}}],
            "attachments": attachments,
        },
        "saveToSentItems": "true",
    }

    url = "https://graph.microsoft.com/v1.0/me/sendMail"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=email_msg)

    if response.status_code == 202:
        print(f"✅ Email sent to {recipient}")
    else:
        print(f"❌ Failed to send email: {response.status_code} {response.text}")


# ------------------------
# Test
# ------------------------
if __name__ == "__main__":
    token = get_token()
    send_email(
        token,
        recipient="someone@example.com",
        subject="Monthly Report 📊",
        body_html="<h2>Hello!</h2><p>Here’s your monthly report attached.</p>",
        onedrive_files=["Documents/report.pdf"],  # list of file paths in OneDrive
    )
