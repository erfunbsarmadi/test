from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive.file"]

def get_sheets_service(creds_json="credentials.json"):
    creds = Credentials.from_service_account_file(creds_json, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)


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


#def write_sheet(spreadsheet_id, range_name, values, creds_json = "credentials.json"):
    """
    Write values to a Google Sheet.
    - spreadsheet_id: The ID of the sheet
    - range_name: e.g. "Sheet1!C2:D2"
    - values: list of lists, e.g. [["Sent", "2025-09-27"]]
    """
   # service = get_sheets_service(creds_json)
   # body = {"values": values}
   # result = service.spreadsheets().values().update(
   #     spreadsheetId=spreadsheet_id,
    #    range=range_name,
    #    valueInputOption="RAW",
    #    body=body
   # ).execute()
   # return result

def write_sheet(spreadsheet_id, range_name, df, creds_json = "credentials.json"):
    """
    Write a pandas DataFrame to a Google Sheet.
    - spreadsheet_id: The ID of the sheet
    - range_name: e.g. "Sheet1!A1"
    - df: pandas DataFrame to write
    """
    service = get_sheets_service(creds_json)

    # Convert DataFrame to list of lists, including headers
    values = [df.columns.tolist()] + df.astype(str).values.tolist()

    body = {"values": values}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()

    print(f"✅ Wrote {len(values)-1} rows and {len(values[0])} columns to {range_name}")
    return result
