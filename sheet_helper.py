from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Scopes needed
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_sheets_service(creds_json):
    """
    Create and return a Sheets API service object.
    """
    creds = Credentials.from_service_account_file(creds_json, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)


def read_sheet(spreadsheet_id, range_name, creds_json):
    """
    Read values from a Google Sheet.
    - spreadsheet_id: The ID of the sheet
    - range_name: e.g. "Sheet1!A2:B10"
    """
    service = get_sheets_service(creds_json)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    return result.get("values", [])


def write_sheet(spreadsheet_id, range_name, values, creds_json):
    """
    Write values to a Google Sheet.
    - spreadsheet_id: The ID of the sheet
    - range_name: e.g. "Sheet1!C2:D2"
    - values: list of lists, e.g. [["Sent", "2025-09-27"]]
    """
    service = get_sheets_service(creds_json)
    body = {"values": values}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()
    return result
