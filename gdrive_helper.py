# gdrive_helper.py (service account version)

import os
import io
from typing import Optional, Union
import json

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google.auth.credentials import Credentials as AuthCredentials

# --------------------------
# Scopes (Drive read/write)
# --------------------------
SCOPES = [
    "https://www.googleapis.com/auth/drive",        # full access
    "https://www.googleapis.com/auth/drive.file",   # files created/opened by service account
]

# --------------------------
# Credential loader
# --------------------------
def _load_creds(creds_or_path: Optional[Union[str, dict, AuthCredentials]] = None):
    """
    Accepts:
      - path to service account JSON (str),
      - the JSON text (str starting with '{') or dict,
      - or a google.auth.credentials.Credentials object.
    Returns: google Credentials object.
    """
    if isinstance(creds_or_path, AuthCredentials):
        return creds_or_path

    if creds_or_path is None:
        return ServiceAccountCredentials.from_service_account_file("credentials.json", scopes=SCOPES)

    if isinstance(creds_or_path, dict):
        return ServiceAccountCredentials.from_service_account_info(creds_or_path, scopes=SCOPES)

    if isinstance(creds_or_path, str):
        s = creds_or_path.strip()
        if s.startswith("{"):
            info = json.loads(s)
            return ServiceAccountCredentials.from_service_account_info(info, scopes=SCOPES)
        else:
            return ServiceAccountCredentials.from_service_account_file(creds_or_path, scopes=SCOPES)

    raise ValueError("creds_or_path must be a path, JSON string/dict, or google Credentials object.")


# --------------------------
# Service helper
# --------------------------
def get_drive_service(creds_or_path: Optional[Union[str, dict, AuthCredentials]] = None):
    creds = _load_creds(creds_or_path)
    return build("drive", "v3", credentials=creds)


# --------------------------
# Download file from Drive
# --------------------------
def download_file(file_id: str, file_path: str, creds_or_path: Optional[Union[str, dict, AuthCredentials]] = None):
    """
    Download a file from Google Drive.
    - file_id: ID of the file in Drive
    - file_path: local path to save the file
    """
    service = get_drive_service(creds_or_path)
    request = service.files().get_media(fileId=file_id)

    fh = io.FileIO(file_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"⬇️ Downloading {os.path.basename(file_path)}: {int(status.progress() * 100)}%")

    print(f"✅ Download complete: {file_path}")


# --------------------------
# Delete local file (after sending email)
# --------------------------
def cleanup_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"🗑️ Removed local file: {file_path}")
