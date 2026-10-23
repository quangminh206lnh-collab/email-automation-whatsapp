
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


    #Sheet1 is the main one
    sheet1 = sheet1.get_all_records()




    # print(f"Spreadsheet: {spreadsheet.title}")
    # print(f"Rows retrieved: {len(sheet1)}")
    # print(type(spreadsheet))
    # for each_row in sheet1:
    #     print(each_row)







if __name__ == "__main__":
    main()
