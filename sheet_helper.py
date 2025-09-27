from googleapiclient.discovery import build
import pandas as pd

def get_sheets_service(creds_json):
    """
    Create and return a Sheets API service object.
    """
    return build("sheets", "v4", credentials=creds_json)


def read_sheet(spreadsheet_id, range_name, creds_json, header=True):
    """
    Read values from a Google Sheet.
    - spreadsheet_id: The ID of the sheet
    - range_name: e.g. "Sheet1!A2:B10"
    """
    service = get_sheets_service(creds_json)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()

    values = result.get("values", [])

    if not values:
        return pd.DataFrame()  # empty sheet → empty df

    # Normalize row lengths to match header length
    header = values[0]
    normalized_rows = [row + [""] * (len(header) - len(row)) for row in values[1:]]

    df = pd.DataFrame(normalized_rows, columns=header)
    return df


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
