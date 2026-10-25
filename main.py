
import os

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
import requests

# Load settings from .env
load_dotenv()


#Define constants
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
CREDENTIALS_FILE = "credentials.json"






#Authenticate with Google using service account credentials
def authenticate():
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
    )

    client = gspread.authorize(credentials)
    return client



#Get data from Google sheet
def get_worksheet_spreadsheet(client):
    """Open the spreadsheet and return its first worksheet."""
    if not SHEET_ID:
        raise ValueError("GOOGLE_SHEET_ID is missing from .env")

    spreadsheet = client.open_by_key(SHEET_ID)
    worksheet = spreadsheet.sheet1


    return spreadsheet, worksheet



#write message to send
def write_message(name,phone_num, date, time, service):
    message = ("This is new customer info:\n"
               f"Name: {name}\n"
               f"Phone: {phone_num}\n"
               f"Date: {date}\n"
               f"Time: {time}\n"
               f"Service: {service}\n")
    return message


#Main program
def main():

    client = authenticate()
    spreadsheet, sheet1 = get_worksheet_spreadsheet(client)
    sheet1_list_of_row  = sheet1.get_all_records()
    for index, row in enumerate (sheet1_list_of_row):
        # this is find the row need to be updated
        if row["Status"] != "Sent":
            sheet1.update_cell(index+2,7, "Sent")
            message = write_message(
                name = row["Name"],
                phone_num=row["Phone number"],
                date=row["Date"],
                time=row["Time"],
                service = row["Service"],)
            print(message)












if __name__ == "__main__":
    main()
