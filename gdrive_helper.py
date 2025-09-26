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
def download_file(file_id, dest_path, service):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(dest_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"Downloading {dest_path}: {int(status.progress() * 100)}%")
    print(f"✅ Download complete: {dest_path}")

# --------------------------
# Upload file
# --------------------------
def upload_file(file_path, mime_type, service, folder_id=None):
    """
    Uploads a file to Google Drive. If a file with the same name exists in the folder,
    it will update the existing file (keeping the same ID). Otherwise, it creates a new file.
    
    Returns the file ID.
    """
    file_name = os.path.basename(file_path)

    # Step 1: Search for existing file in folder
    query = f"name='{file_name}'"
    if folder_id:
        query += f" and '{folder_id}' in parents"

    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])

    media = MediaFileUpload(file_path, mimetype=mime_type)

    if files:
        # File exists → update it
        file_id = files[0]["id"]
        updated_file = service.files().update(
            fileId=file_id,
            media_body=media
        ).execute()
        print(f"🔄 Updated {file_name} → file ID: {file_id}")
        return file_id
    else:
        # File does not exist → create new
        file_metadata = {"name": file_name}
        if folder_id:
            file_metadata["parents"] = [folder_id]

        new_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()
        print(f"✅ Uploaded new {file_name} → file ID: {new_file['id']}")
        return new_file["id"]

# --------------------------
# Delete local file (after sending email)
# --------------------------
def cleanup_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"🗑️ Removed local file: {file_path}")
