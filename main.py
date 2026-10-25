
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

API_TOKEN=os.getenv("API_TOKEN")
PHONE_NUMBER=os.getenv("FROM_PHONE_NUMBER")
TO_PHONE_NUMBER = os.getenv("TO_PHONE_NUMBER")
URL = "https://app.assistro.co/api/v1/wapushplus/single/message"




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


#Send a message to WHATSAPP
def send_whatsapp(phone_number, message):
    if not API_TOKEN:
        raise ValueError("ASSISTRO_API_TOKEN is missing from .env")

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",

    }

    payload = {
        "msgs": [
            {
                "number": phone_number,
                "message": message,
                "type": 1,
            }
        ]
    }

    response = requests.post(
        URL,
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.status_code


def write_message(name,phone_num, date, time, service):
    message = ("This is new customer info:\n"
               f"Name: {name}\n"
               f"Phone  : {phone_num}\n"
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
            try:
                send_whatsapp(TO_PHONE_NUMBER, message)
                sheet1.update_cell(index+2,8, "Sent")
                print(f"Successfully sent the message to {row["Name"]}")
            except requests.RequestException as e:
                sheet1.update_cell(index + 2, 8, "Failed")
                print(f"Failed to send WhatsApp message: {e}")











if __name__ == "__main__":
    main()
