import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io

# --------------------------
# Scopes
# --------------------------
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",  # read/write files created by the app
    "https://www.googleapis.com/auth/drive.readonly",  # read all files
]

# --------------------------
# Service helper
# --------------------------
def get_drive_service(credentials_file="credentials.json", token_file="token.json"):
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    service = build("drive", "v3", credentials=creds)
    return service

# --------------------------
# Download file
# --------------------------
def download_file(file_id, file_path, mime_type=None):
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)

    fh = io.FileIO(file_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"Downloading {os.path.basename(file_path)}: {int(status.progress() * 100)}%")

    print(f"✅ Download complete: {file_path}")

# --------------------------
# Delete local file (after sending email)
# --------------------------
def cleanup_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"🗑️ Removed local file: {file_path}")
