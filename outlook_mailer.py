import os
import base64
import msal
import requests

# === Authentication config ===
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]
CACHE_FILE = "msal_cache.json"


# --------------------------
# Auth helpers
# --------------------------
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
        raise RuntimeError(
            "No valid refresh token in msal_cache.json. Run interactive login locally first."
        )

    save_cache(cache)
    return result["access_token"]

# --------------------------
# Attachment helpers
# --------------------------
def prepare_attachment(file_path):
    """
    Read a file (e.g. PDF) and prepare it for Microsoft Graph attachment format.
    """
    with open(file_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    return {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": os.path.basename(file_path),
        "contentBytes": content,
    }

# --------------------------
# Email sending
# --------------------------
def send_email(token, recipients, subject, body, attachments=None, html=True):
    """
    Send an email with Microsoft Graph API.

    Args:
        token (str): Access token from get_token()
        recipients (list[str]): List of recipient email addresses
        subject (str): Subject of the email
        body (str): Email body (HTML or plain text)
        attachments (list[dict]): List of file dicts like {"name": "file.pdf", "contentBytes": "..."}
        html (bool): Whether the body is HTML (default True)
    """

    url = "https://graph.microsoft.com/v1.0/me/sendMail"

    # Build recipients list
    to_list = [{"emailAddress": {"address": r}} for r in recipients]

    message = {
        "subject": subject,
        "body": {"contentType": "HTML" if html else "Text", "content": body},
        "toRecipients": to_list,
    }

    if attachments:
        #message["attachments"] = attachments
        encoded_attachments = []
        for file_path in attachments:
            encoded_attachments.append(prepare_attachment(file_path))
        message["attachments"] = encoded_attachments

    email_msg = {"message": message, "saveToSentItems": "true"}

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=email_msg)

    if response.status_code == 202:
        print("✅ Email sent successfully!")
        return True
    else:
        print("❌ Failed:", response.status_code, response.text)
        return False

# --------------------------
# Test
# --------------------------
if __name__ == "__main__":
    token = get_token()

    recipients = ["example@domain.com"]
    subject = "Report attached"
    body = "<p>Hello,<br>Here is your PDF report.</p>"

    # Prepare attachments (PDFs you already downloaded from Google Drive)
    attachments = [
        prepare_attachment("report1.pdf"),
        prepare_attachment("report2.pdf"),
    ]

    send_email(token, recipients, subject, body, attachments=attachments)
