# WhatsApp Automation Message

A Python automation project that sends booking details from Google Sheets to a business owner through WhatsApp using the Assistro API.

The goal is to reduce manual work, make booking information easier to access, and demonstrate how Python and APIs can be used to solve practical business problems.

## Overview
This project automates part of the booking process for a small business website I buit and worked on. Customers submit bookings through a Google Form, and their information is stored in Google Sheets. However, the business owner is not familiar with using Google Sheets, so I previously had to manually copy and send booking details to the owner through WhatsApp every day.

As a student, I developed this Python automation to reduce repetitive task. The script retrieves booking details from Google Sheets, formats them into a readable message, and sends them directly to the owner's WhatsApp using the Assistro API. It also tracks processing statuses to help prevent duplicate messages.

The script currently runs manually due to the low volume of bookings, with scheduled execution planned as a future improvement.


## Project Goal
Use automation to make everyday business tasks simpler and quicker to execute.

Rather than requiring the owner to learn another tool, the project send important booking information through WhatsApp, a platform they already use.

## Features

- **Google Sheets integration** — retrieves booking records using `gspread`.
- **WhatsApp messaging** — sends booking details using the Assistro API.
- **Automatic message formatting** — organises customer information into a readable message.
- **Duplicate-send prevention** — skips rows already marked as `Sent`.
- **Status tracking** — updates the corresponding Google Sheets row to `Sent` after a successful HTTP response or `Failed` when a caught HTTP request error occurs.
- **Error handling** — catches request-related errors and prints an error message.
- **Environment variables** — stores API tokens, phone numbers, and spreadsheet configuration outside the main Python script.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language and automation logic |
| `gspread` | Accesses and updates Google Sheets |
| Google Sheets API | Retrieves and updates booking records |
| Google service account authentication | Authenticates access to the spreadsheet |
| `requests` | Sends HTTP POST requests to the Assistro API |
| Assistro API | Sends WhatsApp messages |
| `python-dotenv` | Loads configuration and secrets from a `.env` file |
| `os` | Reads environment variables |
| `google-auth` | Handles Google service account credentials |

## How It Works

The current workflow is:

1. Run the Python script manually.
2. Authenticate with Google Sheets using service account credentials.
3. Open the configured spreadsheet and retrieve booking records.
4. Iterate through the records and skip rows already marked `Sent`.
5. Format the booking information into a WhatsApp message.
6. Send the message using an HTTP POST request to the Assistro API.
7. Update the corresponding status in Google Sheets.
8. Print the result to the terminal and check whether all bookings are marked `Sent`.

### Workflow Diagram

```text
       Run Python Script
               |
               v
    Authenticate with Google
               |
               v
     Retrieve Google Sheets
          Booking Data
               |
               v
       Check Booking Status
               |
          +----+----+
          |         |
      Already      Not Sent
        Sent          |
          |           v
        Skip     Format Message
                      |
                      v
              Assistro API POST
                      |
                +-----+-----+
                |           |
             Success      Request Error
                |           |
                v           v
          Mark "Sent"   Mark "Failed"
                |           |
                +-----+-----+
                      |
                      v
                Next Booking
```

## Example WhatsApp Message

The script formats booking information into a message similar to the following:

```text
This is new customer info:
Name: Example Customer
Phone: 07123456789
Date: 2026-11-01
Time: 14:30
Service: Haircut
```

The actual values are populated from the corresponding Google Sheets row.

## Project Structure

```text
whatsapp-automation-message/
├── main.py
├── .env
├── .env.example
├── .gitignore
├── credentials.json
└── README.md
```

**Important:** `.env` and `credentials.json` are local configuration files and must not be committed to a public repository. The `.gitignore` file should exclude them.

The structure above represents the expected local project layout; secret files should not be included in the public GitHub repository.

## Setup Instructions

### Prerequisites

- Python installed on your computer.
- A Google account with access to the target spreadsheet.
- A Google Cloud project with the Google Sheets API enabled.
- A service account with access to the spreadsheet.
- An Assistro account with API access and a valid API token.

### 1. Clone the Repository

```bash
git clone <...>
cd whatsapp-automation-message
```

Replace `<your-repository-url>` with your actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install gspread python-dotenv google-auth requests
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```dotenv
GOOGLE_SHEET_ID=your_google_sheet_id
API_TOKEN=your_assistro_api_token
TO_PHONE_NUMBER=your_destination_phone_number
```

Replace the example values with your own configuration. Do not commit this file.

### 5. Configure Google Authentication

1. Enable the Google Sheets API in Google Cloud.
2. Create a service account and obtain its JSON credentials.
3. Save the credentials locally as `credentials.json`.
4. Share the target Google spreadsheet with the service account's email address, granting the necessary permissions.

The script uses the Google Sheets scope:

```python
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]
```

This scope allows spreadsheet read and write operations.

### 6. Prepare the Google Sheet

The first worksheet should contain these column headings:

| Name | Phone number | Date | Time | Service | Other fields | Status |
|---|---|---|---|---|---|---|
| Example Customer | 07123456789 | 2026-11-01 | 14:30 | Haircut | — | Pending |

The script expects the columns `Name`, `Phone number`, `Date`, `Time`, and `Service`. It also expects `Status` in column G because the current implementation updates column 7.

Use `Sent` for completed records and another status, such as `Pending`, for records to process.

### 7. Run the Script

```bash
python main.py
```

The script will process eligible rows and print the results in the terminal.

## What I Learned

### 1. Working with APIs

I learned how APIs allow different applications to communicate. This project uses Google Sheets to retrieve and update data and the Assistro API to send WhatsApp messages.

I also gained practical experience with HTTP POST requests, request headers, JSON payloads, response status codes, timeouts, and error handling.

### 2. Authentication and Permissions

I learned how to authenticate with Google Sheets using service account credentials and how an API token can be passed in an HTTP `Authorization` header.

This helped me understand that API access depends on credentials and permissions, rather than simply knowing an endpoint URL.

### 3. Reading Documentation

I practised using documentation to understand how external libraries and APIs work, including the expected request format, authentication requirements, and available methods.

I learned that understanding the documentation is important when connecting services that were developed independently.

### 4. Using AI to Improve Development Efficiency

I used AI as a development assistant to help understand unfamiliar concepts, explore implementation options, explain errors, and improve my code.

Rather than relying only on generated code, I used the process to build my understanding of Python, API requests, and how the different components interact.

### 5. Revisiting Python Fundamentals

This project helped reinforce:

- Functions and passing arguments.
- Dictionaries and lists.
- `for` loops and `enumerate()`.
- Conditional statements.
- Exception handling with `try` and `except`.
- String formatting and f-strings.
- Environment variables and configuration.
- Working with external Python libraries.

### 6. Environment Variables and Security

I learned to keep API tokens and configuration values in environment variables instead of hardcoding them into the Python source code.

I also learned why credential files should be excluded from Git commits and why secrets should never be published in a public repository.

### 7. Business Process Automation

I explored how a relatively small Python program can reduce repetitive administrative work.

By connecting Google Sheets to WhatsApp, the project demonstrates how software can help a business communicate information more efficiently without manually copying and forwarding every booking.

## Challenges and Lessons Learned

Some of the key learning areas included:

- Understanding how Google authentication and service account permissions work.
- Learning the request format expected by an external API.
- Mapping Python list indexes to the correct Google Sheets row numbers.
- Handling request failures without immediately stopping the entire program.
- Keeping track of which bookings have already been processed.

These challenges helped me understand that automation involves more than making an API call: it also requires data handling, error handling, permissions, and reliable status tracking.

## Future Improvements

This project is an ongoing learning experience. The next improvements I want to work towards are:

- **Scheduled execution:** Run the script automatically at regular intervals instead of triggering it manually.
- **Deeper authentication knowledge:** Understand service accounts, API tokens, scopes, permissions, and secure credential management in greater depth.
- **Better documentation skills:** Spend more time reading official API documentation to understand endpoints, request parameters, responses, and limitations before implementation.
- **Cleaner code structure:** Improve naming, separate responsibilities into smaller functions, and make the code easier to maintain.
- **More efficient algorithms:** Improve how records are processed and how spreadsheet updates are handled, including reducing unnecessary API calls.
- **More robust error handling:** Distinguish between different API errors and handle ambiguous outcomes, such as a timeout after a message may already have been accepted.
- **Improved reporting:** Provide a clearer summary of successful, failed, and unprocessed bookings.

## Current Limitations

- The script must currently be run manually.
- The current implementation sends messages to a configured destination phone number.
- It relies on a fixed worksheet layout, including the status column being in column G.
- The script handles HTTP request errors, but a successful HTTP response alone does not necessarily prove that a WhatsApp message was delivered to the recipient.
- Failed records are marked `Failed`, but automatic retries and duplicate-safe recovery have not yet been implemented.

## What This Project Demonstrates

This project demonstrates my ability to combine Python, external APIs, authentication, data processing, and business automation into a practical application.

It also reflects my approach to learning software development: building something useful, researching unfamiliar tools, using AI to improve efficiency, and identifying areas where my understanding and implementation can improve.

The main goal was not just to write a script, but to understand how separate services can work together to solve a real-world problem.

---

**Status:** Working project with manual execution. Scheduled automation and further reliability improvements are planned.
