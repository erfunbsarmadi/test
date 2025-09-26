from gdrive_helper import get_drive_service, download_file, upload_file, cleanup_file
from outlook_mailer import get_token, send_email, prepare_attachment

import mimetypes

# Initialize services
drive_service = get_drive_service()
token = get_token()

# Step 1: Download files from Google Drive
cv_id = "1zvBoRn_5hlhoiSuhptqtD6CdrgxlAryg"
cv = "CV.pdf"
download_file(cv_id, cv, drive_service)

transcripts_id = "1V7eAd-WWpMCW-NDVbapzKUubyCAzLOZH"
transcripts = "Transcripts.pdf"
download_file(transcripts_id, transcripts, drive_service)

emailList_id = "1j3TazOWluMGJZRk9TweKadKpIaE00wZ7coSyjsjcMIQ"
emailList = "emailList.csv"
download_file(emailList_id, emailList, drive_service, mime_type="text/csv")

# Step 2: Send email with attachment
recipients = ["erfanbs1380@gmail.com"]
subject = "Your Report"
body = "<p>Hello,<br>Here is your report PDF.</p>"

attachment = [prepare_attachment(cv), prepare_attachment(transcripts)]
send_email(token, recipients, subject, body, attachments=attachment)

# Step 3 (optional): Upload processed file back to Drive
upload_file(emailList, mimetypes.guess_type(emailList)[0], drive_service)

# Step 4: Clean up local copy
#cleanup_file(cv)
#cleanup_file(transcripts)
#cleanup_file(emailList)
