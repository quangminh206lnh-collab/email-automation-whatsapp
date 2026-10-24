
import os

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# Load settings from .env
load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
CREDENTIALS_FILE = "credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

def authenticate():
    """Authenticate with Google using service account credentials."""
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
    )

    client = gspread.authorize(credentials)
    return client


def get_worksheet_spreadsheet(client):
    """Open the spreadsheet and return its first worksheet."""
    if not SHEET_ID:
        raise ValueError("GOOGLE_SHEET_ID is missing from .env")

    spreadsheet = client.open_by_key(SHEET_ID)
    worksheet = spreadsheet.sheet1


    return spreadsheet, worksheet


def main():
    client = authenticate()
    spreadsheet, sheet1 = get_worksheet_spreadsheet(client)

    sheet1_list_of_row  = sheet1.get_all_records()
    for index, row in enumerate (sheet1_list_of_row):
        # this is find the row need to be updated
        if row["Status"] != "Sent":
            #update the row
            sheet1.update_cell(index+2, 7, "Sent")












if __name__ == "__main__":
    main()
