# sheet_helper.py
import json
import pandas as pd
from typing import Union, Optional
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google.auth.credentials import Credentials as AuthCredentials

# Scopes for Sheets + minimal Drive if you also want to upload files
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]


def _load_creds(creds_or_path: Optional[Union[str, dict, AuthCredentials]] = None):
    """
    Accepts:
      - path to a service account JSON file (str),
      - the JSON text (str starting with '{') or dict,
      - or an already-initialized google.auth.credentials.Credentials object.
    Returns a google Credentials object suitable for googleapiclient.
    """
    # Already a credentials object (user creds or service-account creds)
    if isinstance(creds_or_path, AuthCredentials):
        return creds_or_path

    # If nothing provided, assume default credentials.json file in cwd
    if creds_or_path is None:
        return ServiceAccountCredentials.from_service_account_file("credentials.json", scopes=SCOPES)

    # If dict -> service account info
    if isinstance(creds_or_path, dict):
        return ServiceAccountCredentials.from_service_account_info(creds_or_path, scopes=SCOPES)

    # If string -> could be path or JSON text
    if isinstance(creds_or_path, str):
        s = creds_or_path.strip()
        if s.startswith("{"):
            info = json.loads(s)
            return ServiceAccountCredentials.from_service_account_info(info, scopes=SCOPES)
        else:
            # treat as filepath
            return ServiceAccountCredentials.from_service_account_file(creds_or_path, scopes=SCOPES)

    raise ValueError("creds_or_path must be a path, JSON string/dict, or google Credentials object.")


def get_sheets_service(creds_or_path: Optional[Union[str, dict, AuthCredentials]] = None):
    creds = _load_creds(creds_or_path)
    return build("sheets", "v4", credentials=creds)


def read_sheet(
    spreadsheet_id: str,
    range_name: str,
    creds_or_path: Optional[Union[str, dict, AuthCredentials]] = None,
    header: bool = True,
) -> pd.DataFrame:
    """
    Read values from a Google Sheet into a pandas DataFrame.

    Args:
      - spreadsheet_id: The ID of the spreadsheet.
      - range_name: A1 notation range, e.g. "Sheet1!A1:Z100" or "Sheet1!A2:A".
      - creds_or_path: see _load_creds.
      - header: If True, treat the first row in the returned range as header.
    Returns:
      - pandas.DataFrame
    """
    service = get_sheets_service(creds_or_path)
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    values = result.get("values", [])

    if not values:
        return pd.DataFrame()

    if header and len(values) >= 1:
        header_row = values[0]
        body_rows = values[1:]
    else:
        # No header: create generic column names
        max_cols = max(len(r) for r in values)
        header_row = [f"col{i}" for i in range(1, max_cols + 1)]
        body_rows = values

    # Normalize row lengths to header length
    normalized = [row + [""] * (len(header_row) - len(row)) if len(row) < len(header_row) else row[: len(header_row)] for row in body_rows]

    df = pd.DataFrame(normalized, columns=header_row)
    return df


def write_sheet(
    spreadsheet_id: str,
    range_name: str,
    df: pd.DataFrame,
    creds_or_path: Optional[Union[str, dict, AuthCredentials]] = None,
    overwrite: bool = True,
):
    """
    Write a pandas DataFrame to Google Sheets.

    Args:
      - spreadsheet_id: The ID of the spreadsheet.
      - range_name: Starting cell/range like "Sheet1!A1" (for entire DF include headers).
      - df: pandas DataFrame
      - creds_or_path: see _load_creds
      - overwrite: if True uses 'update' (overwrite). If False uses 'append' (appends rows).
    Returns:
      - API response (dict)
    """
    service = get_sheets_service(creds_or_path)

    # Prepare values with header
    values = [df.columns.tolist()] + df.fillna("").astype(str).values.tolist()

    body = {"values": values}

    if overwrite:
        res = (
            service.spreadsheets()
            .values()
            .update(spreadsheetId=spreadsheet_id, range=range_name, valueInputOption="RAW", body=body)
            .execute()
        )
    else:
        # when appending, range is the sheet name (e.g. "Sheet1")
        res = (
            service.spreadsheets()
            .values()
            .append(spreadsheetId=spreadsheet_id, range=range_name, valueInputOption="RAW", body=body)
            .execute()
        )

    return res

# --------------------------
# Test
# --------------------------
if __name__ == "__main__":
    sheet_id = "1j3TazOWluMGJZRk9TweKadKpIaE00wZ7coSyjsjcMIQ"
    creds_file = "credentials.json"

    #import pandas as pd
    df = read_sheet(sheet_id, "Sheet1!1:1000", creds_file)
    write_sheet(sheet_id, 'Sheet1!A1', df, creds_file)
