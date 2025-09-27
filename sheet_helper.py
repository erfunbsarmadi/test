from googleapiclient.discovery import build

def get_sheet_service(creds):
    """Return an authorized Sheets API service."""
    return build("sheets", "v4", credentials=creds)

def get_data(sheet_id, range_name, creds):
    """
    Read recipient emails from a Google Sheet.

    Args:
        sheet_id (str): Spreadsheet ID.
        range_name (str): e.g., "Recipients!A2:A"
        creds: Google API credentials.

    Returns:
        list of tuples: (row_number, email)
    """
    service = get_sheet_service(creds)
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=range_name
    ).execute()
    values = result.get("values", [])
    
    return values[0]
    
    #recipients = []
    #start_row = int(range_name[1:].split(":")[0])  # e.g. A2 -> 2
    #for i, row in enumerate(values, start=start_row):
    #    if row:
    #        recipients.append((i, row[0]))  # (row_number, email)

    #return recipients

def write_email_status(sheet_id, row, status, creds, column):
    """
    Write back email info (status/message) to a given row.

    Args:
        sheet_id (str): Spreadsheet ID.
        row (int): Row number (starting from 1).
        status (str): Info to write (e.g., "Sent ✅").
        creds: Google API credentials.
        column (str): Column to write into.
    """
    service = get_sheet_service(creds)
    range_name = f"Recipients!{column}{row}"
    body = {"values": [[status]]}
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body,
    ).execute()
