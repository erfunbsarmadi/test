from gdrive_helper import get_drive_service, download_file, upload_file, cleanup_file
from outlook_mailer import get_token, send_email, prepare_attachment

import mimetypes

# Initialize services
drive_service = get_drive_service()
token = get_token()

# Step 1: Download PDF(s) from Google Drive
pdf_id = "YOUR_GOOGLE_DRIVE_FILE_ID"
local_file = "report.pdf"
download_file(pdf_id, local_file, drive_service)

# Step 2: Send email with attachment
recipients = ["example@domain.com"]
subject = "Your Report"
body = "<p>Hello,<br>Here is your report PDF.</p>"

attachment = [prepare_attachment(local_file)]
send_email(token, recipients, subject, body, attachments=attachment)

# Step 3: Clean up local copy
cleanup_file(local_file)

# Step 4 (optional): Upload processed file back to Drive
upload_file("processed_report.pdf", mimetypes.guess_type("processed_report.pdf")[0], drive_service)
